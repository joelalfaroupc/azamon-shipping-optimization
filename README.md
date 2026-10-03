# Azamon — Shipping Optimization with Local Search

Assign parcels to shipping offers while respecting delivery deadlines and weight capacity. The project models the assignment as a constrained search problem and explores **hill climbing** and **simulated annealing** over move and swap neighborhoods.

University team project · **ABIA, Artificial Intelligence degree, FIB–UPC**.

## Problem and implementation

Each parcel has a weight and a priority. Each offer has a maximum load, delivery time and price per unit of weight. Priority levels 0, 1 and 2 allow delivery within 1, 3 and 5 days respectively; earlier delivery is allowed.

`StateRepresentation` stores one parcel list per offer. A move transfers a parcel to another offer; a swap exchanges two parcels. Candidate actions respect both capacity and delivery constraints, and operate on copies of the assignment.

The base objective adds transport cost to storage charges: 0.25 per weight unit for delivery in 3–4 days and 0.50 for day 5. An alternative objective subtracts a weighted early-delivery reward, calculated as `max(0, [1, 2, 4][priority] - delivery_days)` for each parcel.

The standalone runner constructs a feasible initial assignment, then compares best-neighbor hill climbing with a seeded simulated annealing run. Annealing uses a linear temperature schedule from 20 towards 0.01 and retains the best visited state. The output checks that every parcel occurs exactly once and that all capacity and deadline constraints hold.

## Run

Python 3.10+; the standalone demo uses only the standard library.

```sh
python demo.py --parcels 30 --steps 200 --seed 42 --output results/demo.json
python demo.py --objective cost-satisfaction --satisfaction-weight 2 --output results/satisfaction.json
python -m unittest discover -s tests -v
```

## Recorded example

For 30 parcels, 12 offers, seed 42 and the cost objective:

| Assignment | Cost | Feasible |
| --- | ---: | :---: |
| Initial greedy assignment | 382.300 | Yes |
| Hill climbing | 284.975 | Yes |
| Simulated annealing | 305.385 | Yes |

This run reduces the initial cost by approximately 25.5% and 20.1% respectively. It is one reproducible synthetic instance, not a general algorithm ranking or a guarantee of global optimality. Full accepted-state histories are in [results/demo.json](results/demo.json).

## Repository guide and limitations

- `practica.py`: assignment model, feasible neighbors and objectives.
- `demo.py`: independent search implementations and result export.
- `abia_azamon.py`: original course instance-generation utilities.
- `archive/`: preserved source snapshot, including the original AIMA-oriented scripts.
- `tests/`: regression checks for empty offers, state copying and initialization.

Greedy initialization can fail even when another assignment would be feasible. Neighbor enumeration becomes expensive for large instances. The archived AIMA scripts require their original external framework; the standalone demo is the supported entry point.

The portfolio edition corrects empty-offer capacity accounting, allows early delivery during initialization and removes candidate-construction side effects from iteration logging. Original files remain in `archive/`.

## Credits and source

Academic group work, preserved from [daniupc/azamon](https://github.com/daniupc/azamon). That upstream repository may require access. The archive is a recovered subset, not a complete copy of every original experiment. Course-provided utilities retain their original attribution. See [PROVENANCE.md](PROVENANCE.md) for the source manifest.
