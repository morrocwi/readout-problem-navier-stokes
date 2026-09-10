#!/usr/bin/env python3
"""Exact K=2 scalar-energy observability witness over F_251.

The finite cubic truncation K_2 has 124 nonzero modes and 248 real
incompressible degrees of freedom. Translation symmetry caps generic local
energy-jet rank at 245. A scalar jet cannot reach 245 before R=244.

This checker propagates the formal Taylor state and 245 projected tangent
directions exactly modulo p=251. Because p>244 and all Galerkin/basis/
viscosity denominators are invertible mod p, Taylor and Lie-jet ranks agree
through order 244 up to invertible factorial scalings. If the projected
245x245 Jacobian has rank 245 at R=244, then the full Jacobian has row rank
245 over F_p; hence a characteristic-zero maximal minor is not identically
zero. Positive-viscosity scaling then transfers the generic rank statement to
all nu>0.

Requires numpy and numba. A typical 5-thread CPU run takes several minutes.
"""
import itertools, json, time
import numpy as np
from numba import njit, prange, get_num_threads

P=251; N=2; RMAX=244; BATCH=245
SEED_STATE=20260910; SEED_PROJ=20260911
vals=range(-N,N+1)
modes=[k for k in itertools.product(vals,repeat=3) if k!=(0,0,0)]
mode_index={k:i for i,k in enumerate(modes)}
reps=[k for k in modes if next(v for v in k if v!=0)>0]
rep_index={k:i for i,k in enumerate(reps)}
nm=len(modes); nr=len(reps); d=4*nr

def basis(k):
    kv=np.array(k,dtype=np.int64)
    for axis in (np.array((1,0,0),dtype=np.int64),np.array((0,1,0),dtype=np.int64),np.array((0,0,1),dtype=np.int64)):
        e1=np.cross(kv,axis)
        if np.any(e1!=0): break
    e2=np.cross(kv,e1)
    return e1,e2,int(e1@e1),int(e2@e2)

bases=[basis(k) for k in reps]
E1=np.array([b[0] for b in bases],dtype=np.int64)%P
E2=np.array([b[1] for b in bases],dtype=np.int64)%P
invn1=np.array([pow(b[2],-1,P) for b in bases],dtype=np.int64)
invn2=np.array([pow(b[3],-1,P) for b in bases],dtype=np.int64)
reps_arr=np.array(reps,dtype=np.int64); modes_arr=np.array(modes,dtype=np.int64)
full_rep=np.empty(nm,dtype=np.int64); full_sign=np.empty(nm,dtype=np.int64)
for mi,k in enumerate(modes):
    if next(v for v in k if v!=0)>0: rk,s=k,1
    else: rk,s=tuple(-v for v in k),-1
    full_rep[mi]=rep_index[rk]; full_sign[mi]=s
starts=[0]; tp=[]; tq=[]
for k in reps:
    for p in modes:
        q=tuple(k[j]-p[j] for j in range(3)); qi=mode_index.get(q)
        if qi is not None: tp.append(mode_index[p]); tq.append(qi)
    starts.append(len(tp))
starts=np.array(starts,dtype=np.int64); tp=np.array(tp,dtype=np.int64); tq=np.array(tq,dtype=np.int64)
k2rep=np.array([sum(v*v for v in k) for k in reps],dtype=np.int64)
invk2=np.array([pow(int(v),-1,P) for v in k2rep],dtype=np.int64)
nu_mod=pow(200,-1,P)
lin_diag=np.repeat((-nu_mod*k2rep)%P,4).astype(np.int64)
shells=sorted(set(int(v) for v in k2rep))
shell_index={q:i for i,q in enumerate(shells)}
weights=np.zeros((len(shells),d),dtype=np.int64)
for ri,k in enumerate(reps):
    si=shell_index[sum(v*v for v in k)]; n1,n2=bases[ri][2],bases[ri][3]
    weights[si,4*ri:4*ri+2]=n1%P; weights[si,4*ri+2:4*ri+4]=n2%P
total_weight=np.sum(weights,axis=0)%P
E1u=E1.astype(np.uint16); E2u=E2.astype(np.uint16)
invn1u=invn1.astype(np.uint16); invn2u=invn2.astype(np.uint16); invk2u=invk2.astype(np.uint16)
linu=lin_diag.astype(np.uint16); twu=total_weight.astype(np.uint16)

@njit(cache=True)
def recon_one(x,U,full_rep,full_sign,E1,E2,P):
    for mi in range(full_rep.shape[0]):
        ri=full_rep[mi]; s=full_sign[mi]
        ar=np.int64(x[4*ri]); ai=np.int64(x[4*ri+1]); br=np.int64(x[4*ri+2]); bi=np.int64(x[4*ri+3])
        if s<0: ai=(-ai)%P; bi=(-bi)%P
        for c in range(3):
            e1=np.int64(E1[ri,c]); e2=np.int64(E2[ri,c])
            U[mi,c,0]=(ar*e1+br*e2)%P; U[mi,c,1]=(ai*e1+bi*e2)%P

@njit(parallel=True,cache=True)
def recon_batch(V,UV,full_rep,full_sign,E1,E2,P):
    for bb in prange(V.shape[0]): recon_one(V[bb],UV[bb],full_rep,full_sign,E1,E2,P)

@njit(cache=True)
def project(vr0,vr1,vr2,vi0,vi1,vi2,ri,reps_arr,E1,E2,invn1,invn2,invk2,P,out):
    vr0%=P; vr1%=P; vr2%=P; vi0%=P; vi1%=P; vi2%=P
    k0=reps_arr[ri,0]; k1=reps_arr[ri,1]; k2=reps_arr[ri,2]
    qr0=vi0; qr1=vi1; qr2=vi2; qi0=(-vr0)%P; qi1=(-vr1)%P; qi2=(-vr2)%P
    dr=(qr0*k0+qr1*k1+qr2*k2)%P; di=(qi0*k0+qi1*k1+qi2*k2)%P; inv=np.int64(invk2[ri])
    pr0=(qr0-dr*k0*inv)%P; pr1=(qr1-dr*k1*inv)%P; pr2=(qr2-dr*k2*inv)%P
    pi0=(qi0-di*k0*inv)%P; pi1=(qi1-di*k1*inv)%P; pi2=(qi2-di*k2*inv)%P
    e10=np.int64(E1[ri,0]);e11=np.int64(E1[ri,1]);e12=np.int64(E1[ri,2]);e20=np.int64(E2[ri,0]);e21=np.int64(E2[ri,1]);e22=np.int64(E2[ri,2])
    in1=np.int64(invn1[ri]); in2=np.int64(invn2[ri])
    out[4*ri]=((pr0*e10+pr1*e11+pr2*e12)%P)*in1%P
    out[4*ri+1]=((pi0*e10+pi1*e11+pi2*e12)%P)*in1%P
    out[4*ri+2]=((pr0*e20+pr1*e21+pr2*e22)%P)*in2%P
    out[4*ri+3]=((pi0*e20+pi1*e21+pi2*e22)%P)*in2%P

@njit(cache=True)
def state_rhs(n,xcoef,Ux,lin_diag,starts,tp,tq,modes_arr,reps_arr,E1,E2,invn1,invn2,invk2,P):
    out=np.empty(4*reps_arr.shape[0],dtype=np.uint16); tmp=np.zeros(out.shape[0],dtype=np.int64)
    for ri in range(reps_arr.shape[0]):
        vr0=vr1=vr2=vi0=vi1=vi2=np.int64(0)
        for i in range(n+1):
            j=n-i
            for tt in range(starts[ri],starts[ri+1]):
                pi=tp[tt]; qi=tq[tt]; q0=modes_arr[qi,0]; q1=modes_arr[qi,1]; q2=modes_arr[qi,2]
                sr=np.int64(Ux[i,pi,0,0])*q0+np.int64(Ux[i,pi,1,0])*q1+np.int64(Ux[i,pi,2,0])*q2
                si=np.int64(Ux[i,pi,0,1])*q0+np.int64(Ux[i,pi,1,1])*q1+np.int64(Ux[i,pi,2,1])*q2
                br=np.int64(Ux[j,qi,0,0]); bi=np.int64(Ux[j,qi,0,1]); vr0 += sr*br-si*bi; vi0 += sr*bi+si*br
                br=np.int64(Ux[j,qi,1,0]); bi=np.int64(Ux[j,qi,1,1]); vr1 += sr*br-si*bi; vi1 += sr*bi+si*br
                br=np.int64(Ux[j,qi,2,0]); bi=np.int64(Ux[j,qi,2,1]); vr2 += sr*br-si*bi; vi2 += sr*bi+si*br
        project(vr0,vr1,vr2,vi0,vi1,vi2,ri,reps_arr,E1,E2,invn1,invn2,invk2,P,tmp)
    for c in range(out.shape[0]): out[c]=(np.int64(xcoef[n,c])*np.int64(lin_diag[c])+tmp[c])%P
    return out

@njit(parallel=True,cache=True)
def tangent_rhs(n,Vcoef,UV,Ux,lin_diag,starts,tp,tq,modes_arr,reps_arr,E1,E2,invn1,invn2,invk2,P):
    batch=Vcoef.shape[1]; out=np.empty((batch,4*reps_arr.shape[0]),dtype=np.uint16)
    for bb in prange(batch):
        tmp=np.zeros(out.shape[1],dtype=np.int64)
        for ri in range(reps_arr.shape[0]):
            vr0=vr1=vr2=vi0=vi1=vi2=np.int64(0)
            for i in range(n+1):
                j=n-i
                for tt in range(starts[ri],starts[ri+1]):
                    pi=tp[tt]; qi=tq[tt]; q0=modes_arr[qi,0]; q1=modes_arr[qi,1]; q2=modes_arr[qi,2]
                    sr=np.int64(UV[i,bb,pi,0,0])*q0+np.int64(UV[i,bb,pi,1,0])*q1+np.int64(UV[i,bb,pi,2,0])*q2
                    si=np.int64(UV[i,bb,pi,0,1])*q0+np.int64(UV[i,bb,pi,1,1])*q1+np.int64(UV[i,bb,pi,2,1])*q2
                    br=np.int64(Ux[j,qi,0,0]); bi=np.int64(Ux[j,qi,0,1]); vr0 += sr*br-si*bi; vi0 += sr*bi+si*br
                    br=np.int64(Ux[j,qi,1,0]); bi=np.int64(Ux[j,qi,1,1]); vr1 += sr*br-si*bi; vi1 += sr*bi+si*br
                    br=np.int64(Ux[j,qi,2,0]); bi=np.int64(Ux[j,qi,2,1]); vr2 += sr*br-si*bi; vi2 += sr*bi+si*br
                    sr=np.int64(Ux[j,pi,0,0])*q0+np.int64(Ux[j,pi,1,0])*q1+np.int64(Ux[j,pi,2,0])*q2
                    si=np.int64(Ux[j,pi,0,1])*q0+np.int64(Ux[j,pi,1,1])*q1+np.int64(Ux[j,pi,2,1])*q2
                    br=np.int64(UV[i,bb,qi,0,0]); bi=np.int64(UV[i,bb,qi,0,1]); vr0 += sr*br-si*bi; vi0 += sr*bi+si*br
                    br=np.int64(UV[i,bb,qi,1,0]); bi=np.int64(UV[i,bb,qi,1,1]); vr1 += sr*br-si*bi; vi1 += sr*bi+si*br
                    br=np.int64(UV[i,bb,qi,2,0]); bi=np.int64(UV[i,bb,qi,2,1]); vr2 += sr*br-si*bi; vi2 += sr*bi+si*br
            project(vr0,vr1,vr2,vi0,vi1,vi2,ri,reps_arr,E1,E2,invn1,invn2,invk2,P,tmp)
        for c in range(out.shape[1]): out[bb,c]=(np.int64(Vcoef[n,bb,c])*np.int64(lin_diag[c])+tmp[c])%P
    return out

@njit(parallel=True,cache=True)
def energy_row(n,Vcoef,xcoef,total_weight,P):
    row=np.empty(Vcoef.shape[1],dtype=np.uint16)
    for bb in prange(Vcoef.shape[1]):
        acc=np.int64(0)
        for i in range(n+1):
            j=n-i
            for c in range(Vcoef.shape[2]): acc += 2*np.int64(total_weight[c])*np.int64(Vcoef[i,bb,c])*np.int64(xcoef[j,c])
        row[bb]=acc%P
    return row

def rank_mod(A,p=P):
    A=np.asarray(A,dtype=np.int64).copy()%p; rows,cols=A.shape; r=0
    for col in range(cols):
        piv=next((rr for rr in range(r,rows) if A[rr,col]%p),None)
        if piv is None: continue
        if piv!=r: A[[r,piv]]=A[[piv,r]]
        A[r]=A[r]*pow(int(A[r,col]),-1,p)%p
        for rr in range(r+1,rows):
            if A[rr,col]: A[rr]=(A[rr]-A[rr,col]*A[r])%p
        r+=1
        if r==min(rows,cols): break
    return r

def main():
    assert P>RMAX and d==248 and len(modes)==124 and BATCH==d-3
    print(f'K=2 exact modular observability: modes={nm} d={d} shells={shells} prime={P} threads={get_num_threads()}',flush=True)
    rng=np.random.default_rng(SEED_STATE)
    xcoef=np.zeros((RMAX+1,d),dtype=np.uint16); Ux=np.zeros((RMAX+1,nm,3,2),dtype=np.uint16)
    xcoef[0]=rng.integers(1,P,size=d,dtype=np.uint16); recon_one(xcoef[0],Ux[0],full_rep,full_sign,E1u,E2u,P)
    _=state_rhs(0,xcoef,Ux,linu,starts,tp,tq,modes_arr,reps_arr,E1u,E2u,invn1u,invn2u,invk2u,P)
    t=time.time()
    for n in range(RMAX):
        rhs=state_rhs(n,xcoef,Ux,linu,starts,tp,tq,modes_arr,reps_arr,E1u,E2u,invn1u,invn2u,invk2u,P)
        xcoef[n+1]=(rhs.astype(np.int64)*pow(n+1,-1,P)%P).astype(np.uint16)
        recon_one(xcoef[n+1],Ux[n+1],full_rep,full_sign,E1u,E2u,P)
    state_sec=time.time()-t
    rng=np.random.default_rng(SEED_PROJ)
    Vcoef=np.zeros((RMAX+1,BATCH,d),dtype=np.uint16); UV=np.zeros((RMAX+1,BATCH,nm,3,2),dtype=np.uint16)
    Vcoef[0]=rng.integers(0,P,size=(BATCH,d),dtype=np.uint16); recon_batch(Vcoef[0],UV[0],full_rep,full_sign,E1u,E2u,P)
    _=tangent_rhs(0,Vcoef,UV,Ux,linu,starts,tp,tq,modes_arr,reps_arr,E1u,E2u,invn1u,invn2u,invk2u,P)
    O=np.zeros((RMAX+1,BATCH),dtype=np.uint16); O[0]=energy_row(0,Vcoef,xcoef,twu,P)
    milestones={}; t=time.time()
    for n in range(RMAX):
        rhs=tangent_rhs(n,Vcoef,UV,Ux,linu,starts,tp,tq,modes_arr,reps_arr,E1u,E2u,invn1u,invn2u,invk2u,P)
        Vcoef[n+1]=(rhs.astype(np.int64)*pow(n+1,-1,P)%P).astype(np.uint16)
        recon_batch(Vcoef[n+1],UV[n+1],full_rep,full_sign,E1u,E2u,P)
        O[n+1]=energy_row(n+1,Vcoef,xcoef,twu,P)
        R=n+1
        if R in (10,30,60,120,180,220,243,244):
            rk=rank_mod(O[:R+1]); milestones[R]={'rank':rk,'elapsed_sec':round(time.time()-t,3)}
            print(f'R={R} rank={rk} elapsed={time.time()-t:.1f}s',flush=True)
    tangent_sec=time.time()-t; final_rank=rank_mod(O)
    result={'status':'PASS' if final_rank==245 else 'FAIL','N':2,'prime':P,'viscosity':'1/200','mode_count':nm,'real_state_dimension':d,'shells':shells,'translation_ceiling':245,'scalar_min_possible_order':244,'projection_columns':BATCH,'state_seed':SEED_STATE,'projection_seed':SEED_PROJ,'final_rank_R244':final_rank,'milestones':milestones,'state_series_sec':state_sec,'tangent_series_sec':tangent_sec,'numba_threads':get_num_threads()}
    print('RESULT_JSON:'+json.dumps(result,sort_keys=True),flush=True)
    return 0 if final_rank==245 else 1

if __name__=='__main__': raise SystemExit(main())
