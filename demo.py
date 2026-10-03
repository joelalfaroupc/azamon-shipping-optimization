"""Standalone runners for the academic move/swap neighborhood."""
import argparse, json, math, random
import config
from pathlib import Path
from abia_azamon import random_paquetes, random_ofertas
from practica import generate_initial_state1

def valid(state, parcels):
    assigned = [p for group in state.state for p in group]
    return (sorted(map(id, assigned)) == sorted(map(id, parcels))
            and all(sum(p.peso for p in group) <= o.pesomax + 1e-9
                    and all(state.asignable(p, o) for p in group)
                    for group, o in zip(state.state, state.ofertas)))

def search(initial, algorithm, steps, seed, objective):
    rng = random.Random(seed)
    score = lambda s: s.heuristic() if objective == 'cost' else s.heuristic00()
    state = best = initial
    history = [score(state)]
    for step in range(steps):
        actions = list(state.generate_actions())
        if not actions:
            break
        if algorithm == 'hill-climbing':
            candidate = min((state.apply_action(a) for a in actions), key=score)
            if score(candidate) >= score(state) - 1e-12:
                break
            state = candidate
        else:
            candidate = state.apply_action(rng.choice(actions))
            delta = score(candidate) - score(state)
            temperature = max(.01, 20 * (1 - step / steps))
            if delta <= 0 or rng.random() < math.exp(-delta / temperature):
                state = candidate
        if score(state) < score(best):
            best = state
        history.append(score(state))
    return best, history

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--parcels', type=int, default=30)
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--steps', type=int, default=200)
    parser.add_argument('--objective', choices=['cost','cost-satisfaction'], default='cost')
    parser.add_argument('--satisfaction-weight', type=float, default=1.0)
    parser.add_argument('--output', default='results/demo.json')
    args = parser.parse_args()
    if args.parcels < 1 or args.steps < 1: parser.error('positive parcels/steps required')
    if not math.isfinite(args.satisfaction_weight) or args.satisfaction_weight < 0:
        parser.error('satisfaction weight must be finite and nonnegative')
    config.ponderacion_felicidad = args.satisfaction_weight
    parcels = random_paquetes(args.parcels, args.seed)
    offers = random_ofertas(parcels, 1.5, args.seed)
    initial = generate_initial_state1(parcels, offers)
    assert valid(initial, parcels)
    results = {'seed':args.seed,'parcels':args.parcels,'offers':len(offers),
               'objective':args.objective,'satisfaction_weight':args.satisfaction_weight,
               'initial_cost':initial.heuristic(),'algorithms':{}}
    for algorithm in ['hill-climbing','simulated-annealing']:
        best, history = search(initial, algorithm, args.steps, args.seed, args.objective)
        assert valid(best, parcels)
        results['algorithms'][algorithm] = {'cost':best.heuristic(),
          'objective':best.heuristic() if args.objective == 'cost' else best.heuristic00(),
          'accepted_state_history':history,'feasible':True}
    path = Path(args.output); path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps({k:v for k,v in results.items() if k!='algorithms'}))
    for name, result in results['algorithms'].items(): print(name,result['cost'],result['feasible'])

if __name__ == '__main__': main()
