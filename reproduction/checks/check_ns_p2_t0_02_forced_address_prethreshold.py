#!/usr/bin/env python3
"""Pre-threshold forced-address audit of the T0-02 runtime record (point A, depth d = 2).

Question: does the numerical pipeline respect the per-address
accounting BEFORE its 1e-12 * B(T0) retention threshold is applied?  A registered address that
carries forcing F(a) != 0 while its amplitude is zero is FORGOTTEN_REGISTERED; the T0-02 report
states Dropped = T = 0 at every window end, and this checker looks at the layer underneath that
readout.

Input: reproduction/data/ns_p2_t0_02_A_d2_prethreshold.json, a compact export of the internal run
record rg_t0_02_A_d2.npz (T0-2026-09-12-02).  At the four stored reader-window boundaries
(t = 0, tau, 2tau, 3tau) the forcing N_k on every registered address was recomputed in float64 from
the stored full state with the stepper's own pair table (no threshold applied); a fifth sample at
the first record (t = rec*dt) comes from the run's recorded Nhist (complex64) / load_hist (float64)
arrays and is labelled as such.  Every float is written with 6 significant digits; 0.0 is kept
exactly; NO rational rounding is applied to any value used in a decision.

Float semantics (declared, never renamed EXACT):
  amplitude zero     : bitwise zero (uabs == 0.0 where the state is stored, else load == 0.0);
                       "below the run's retention threshold" (0 < load <= 1e-12 * B(T0)) is a
                       separate sub-count and is NOT amplitude zero;
  forcing zero       : NUMERICAL_ZERO(eps) with eps = 1e-12 on max_c |F_c|; the bitwise-zero
                       sub-count is reported inside it;
  states             : ACTIVE (amplitude bitwise nonzero) > NUMERICAL_ZERO(eps) (amplitude zero,
                       |F| <= eps) > FORGOTTEN_REGISTERED (amplitude zero, |F| > eps).
A second, deliberately stricter reading ("threshold semantics": amplitude := load > threshold) is
reported next to it so the two readers can be compared; it is not the accounting semantics.

As a comparison only, the number of nonzero float components that Fraction.limit_denominator(10**9)
would round to exactly 0 is printed: this is why rational rounding is not used for a zero decision.

Exit addresses S_{d+1} \\ S_d are unregistered and outside the declared cell (TED by construction);
their per-window Duhamel-load counts are reported from the export.  Tier: finite_diagnostic.  This
audit proves nothing about OCSR, Witness Soundness, G6/G7 or Clay Navier-Stokes regularity.
"""
import json
import sys
import time
from fractions import Fraction
from pathlib import Path

T0 = time.time()
EPS_F = 1e-12
DATA = Path(__file__).resolve().parents[1] / 'data' / 'ns_p2_t0_02_A_d2_prethreshold.json'

# Calibration against the internal record (bitwise semantics unless stated).  Any change in the
# data file that moves these counts must be explained, not silently accepted.
EXPECTED = {
    'snap_0':   {'t': 0.0,        'ACTIVE': 7,   'NUMERICAL_ZERO': 259, 'NUMERICAL_ZERO_bitwise': 256, 'FORGOTTEN_REGISTERED': 23, 'below_threshold': 0,   'threshold_forgotten': 23},
    'record_1': {'t': 0.003,      'ACTIVE': 289, 'NUMERICAL_ZERO': 0,   'NUMERICAL_ZERO_bitwise': 0,   'FORGOTTEN_REGISTERED': 0,  'below_threshold': 187, 'threshold_forgotten': 187},
    'snap_1':   {'t': 5.350422,   'ACTIVE': 289, 'NUMERICAL_ZERO': 0,   'NUMERICAL_ZERO_bitwise': 0,   'FORGOTTEN_REGISTERED': 0,  'below_threshold': 0,   'threshold_forgotten': 0},
    'snap_2':   {'t': 10.70084,   'ACTIVE': 289, 'NUMERICAL_ZERO': 0,   'NUMERICAL_ZERO_bitwise': 0,   'FORGOTTEN_REGISTERED': 0,  'below_threshold': 0,   'threshold_forgotten': 0},
    'snap_3':   {'t': 16.04977,   'ACTIVE': 289, 'NUMERICAL_ZERO': 0,   'NUMERICAL_ZERO_bitwise': 0,   'FORGOTTEN_REGISTERED': 0,  'below_threshold': 0,   'threshold_forgotten': 0},
}


def classify_sample(s, addresses, thr):
    F = s['F']; load = s['load']; uabs = s.get('uabs')
    recs = []
    for j, a in enumerate(addresses):
        Fabs = max(abs(complex(re, im)) for re, im in F[j])
        amp_bitwise_zero = (uabs[j] == 0.0) if uabs is not None else (load[j] == 0.0)
        if uabs is not None:
            assert (uabs[j] == 0.0) == (load[j] == 0.0), (s['label'], a['a'])   # consistency of the export
        below_thr = (not amp_bitwise_zero) and load[j] <= thr
        if not amp_bitwise_zero:
            st = 'ACTIVE'
        elif Fabs <= EPS_F:
            st = 'NUMERICAL_ZERO'
        else:
            st = 'FORGOTTEN_REGISTERED'
        # threshold semantics (comparison reader): amplitude := load > thr
        if load[j] > thr:
            st_thr = 'ACTIVE'
        elif Fabs <= EPS_F:
            st_thr = 'NUMERICAL_ZERO'
        else:
            st_thr = 'FORGOTTEN_REGISTERED'
        recs.append(dict(a=tuple(a['a']), gen=a['gen'], cell=a['cell'], N=None, F=F[j], Fabs=Fabs,
                         F_bitwise_zero=(Fabs == 0.0), registered=True, load=load[j], amp_bitwise_zero=amp_bitwise_zero,
                         below_threshold=below_thr, state=st, state_threshold_reader=st_thr, eps=EPS_F))
    return recs


def rational_rounding_count(s):
    n_nonzero = n_rounds_to_zero = 0
    for f in s['F']:
        for re, im in f:
            for x in (re, im):
                if x != 0.0:
                    n_nonzero += 1
                    if Fraction(x).limit_denominator(10 ** 9) == 0:
                        n_rounds_to_zero += 1
    return n_nonzero, n_rounds_to_zero


def main():
    d = json.loads(DATA.read_text())
    assert d['record'] == 'T0-2026-09-12-02' and d['tier'] == 'finite_diagnostic'
    thr = d['source_run']['load_tol_abs']
    B_T0 = d['source_run']['B_T0']
    assert abs(thr - 1e-12 * B_T0) <= 1e-6 * thr, (thr, B_T0)
    addresses = d['addresses']
    assert len(addresses) == d['source_run']['N_half'] == 289
    print(f"T0-02 point A d=2: N_half={len(addresses)} B(T0)={B_T0} retention threshold={thr:.3e} eps_F={EPS_F:.0e}")
    print(f"rounding of the export: {d['rounding']}")
    print()
    print(f"{'sample':9s} {'t':>10s} {'ACTIVE':>7s} {'(below thr)':>11s} {'NUM_ZERO':>9s} {'(bitwise0)':>10s} {'FORGOTTEN_REG':>13s} | {'thr-reader FORGOTTEN':>20s}  source")
    out = {'tier': 'finite_diagnostic', 'eps_F': EPS_F, 'retention_threshold': thr, 'samples': []}
    for s in d['samples']:
        recs = classify_sample(s, addresses, thr)
        n = lambda st: sum(1 for r in recs if r['state'] == st)
        n_active = n('ACTIVE'); n_nz = n('NUMERICAL_ZERO'); n_fr = n('FORGOTTEN_REGISTERED')
        n_below = sum(1 for r in recs if r['below_threshold'])
        n_bit0 = sum(1 for r in recs if r['state'] == 'NUMERICAL_ZERO' and r['F_bitwise_zero'])
        n_thr_fr = sum(1 for r in recs if r['state_threshold_reader'] == 'FORGOTTEN_REGISTERED')
        assert n_active + n_nz + n_fr == len(addresses)
        print(f"{s['label']:9s} {s['t']:10.6f} {n_active:7d} {n_below:11d} {n_nz:9d} {n_bit0:10d} {n_fr:13d} | {n_thr_fr:20d}  {s['source'].split(';')[0]}")
        e = EXPECTED[s['label']]
        assert abs(s['t'] - e['t']) < 1e-3, (s['label'], s['t'])
        got = (n_active, n_nz, n_bit0, n_fr, n_below, n_thr_fr)
        exp = (e['ACTIVE'], e['NUMERICAL_ZERO'], e['NUMERICAL_ZERO_bitwise'], e['FORGOTTEN_REGISTERED'], e['below_threshold'], e['threshold_forgotten'])
        assert got == exp, (s['label'], got, exp)
        if s['t'] > 0:
            assert n_fr == 0, (s['label'], n_fr)              # the pipeline carries every forced address it registers
        else:
            forg = [r for r in recs if r['state'] == 'FORGOTTEN_REGISTERED']
            gens = sorted({r['gen'] for r in forg})
            assert gens == [1], gens                              # at the datum instant only generation-1 addresses are forced and empty
            assert all(r['gen'] == 0 for r in recs if r['state'] == 'ACTIVE')
            tiny = [r for r in recs if r['state'] == 'NUMERICAL_ZERO' and not r['F_bitwise_zero']]
            assert len(tiny) == 3 and all(r['Fabs'] < 1e-15 for r in tiny), [(r['a'], r['Fabs']) for r in tiny]
            print(f"  t = 0: forced-and-empty addresses (all generation 1): {[list(r['a']) for r in forg]}")
            print(f"  t = 0: NUMERICAL_ZERO but not bitwise zero (roundoff at geometrically null datum targets, NULL_BY_GEOMETRY in the exact W3A fixture): {[(list(r['a']), '%.1e' % r['Fabs']) for r in tiny]}")
        n_nonzero, n_r0 = rational_rounding_count(s)
        out['samples'].append({'label': s['label'], 't': s['t'], 'ACTIVE': n_active, 'ACTIVE_below_threshold': n_below,
                               'NUMERICAL_ZERO': n_nz, 'NUMERICAL_ZERO_bitwise': n_bit0, 'FORGOTTEN_REGISTERED': n_fr,
                               'threshold_reader_FORGOTTEN_REGISTERED': n_thr_fr,
                               'rational_rounding': {'nonzero_float_components': n_nonzero, 'rounded_to_zero_by_limit_denominator_1e9': n_r0},
                               'forgotten_addresses': [list(r['a']) for r in recs if r['state'] == 'FORGOTTEN_REGISTERED'],
                               'records': recs})
    print()
    for smp in out['samples']:
        rr = smp['rational_rounding']
        print(f"rational-rounding comparison {smp['label']:9s}: {rr['rounded_to_zero_by_limit_denominator_1e9']} of {rr['nonzero_float_components']} nonzero float components would become exactly 0 under Fraction.limit_denominator(10**9)")
    ex = d['exit_layer']
    print()
    print('exit layer (unregistered, outside the declared cell = TED by construction), Duhamel window loads:')
    for w in ex['windows']:
        print(f"  window {w['window']}: exit half addresses={w['n_exit_half']} nonzero(bitwise)={w['n_nonzero_bitwise']} above 1e-12={w['n_above_1e-12']} max|I|={w['max_abs']}")
        assert w['n_above_1e-12'] > 0
    print()
    print('reading: at t = 0 the datum leaves the generation-1 targets forced and empty (the addresses the first step')
    print('populates); at every t > 0 sample no registered address is forced and empty (FORGOTTEN_REGISTERED = 0);')
    print('at t = 0.003 the threshold reader would call 187 sub-threshold addresses "not energised" although the')
    print('pipeline carries them (nonzero amplitude) -- a reader artefact, not an accounting omission.')
    out['wall_s'] = round(time.time() - T0, 2)
    if '--json' in sys.argv:
        json.dump(out, open(sys.argv[sys.argv.index('--json') + 1], 'w'), indent=1, default=str)
    print(f'NS P2 T0-02 PRE-THRESHOLD FORCED-ADDRESS AUDIT PASS in {out["wall_s"]}s')


if __name__ == '__main__':
    main()
