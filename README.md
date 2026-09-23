# Enigma and Bombe Simulator

This project is a Python recreation of two historically important machines:

- the German **Enigma** cipher machine
- the **Bombe**, the codebreaking device associated with Alan Turing and Bletchley Park

The goal of the repository is to model how Enigma encryption works and to explore how a Bombe-style search can help recover machine settings from known plaintext and ciphertext pairs. The project is intended as an educational software model of the machines and their codebreaking workflow.

## What is in the project

- `enigma.py` contains the Enigma simulator.
- `bombe.py` contains the Bombe-style analysis and search logic.

Both scripts use hardcoded Enigma I rotor, reflector, and entry-wheel wirings based on the service machine used by the German Army and Air Force. The current examples use three rotors, reflector B, zero ring settings, and a fixed example plugboard configuration.

## How the machines work together

1. Enigma encrypts a message by passing each letter through the plugboard, rotors, reflector, and rotors again in reverse.
2. The rotors step between key presses, changing the substitution for the next letter.
3. The Bombe uses a known plaintext/ciphertext relationship to build a menu of connected letter relationships.
4. Candidate rotor positions and plugboard hypotheses are tested, allowing inconsistent settings to be rejected.

## Enigma simulator

The Enigma script currently demonstrates:

- rotor-based substitution encryption
- reflector-based return path
- plugboard swapping
- rotor stepping and turnover behavior

The example currently encrypts `HELLOWORLDIAMBOB` and prints ciphertext and internal machine state to the console. Input values and machine settings are currently defined in the source code rather than collected interactively.

## Bombe implementation

The Bombe script currently demonstrates:

- menu building from plaintext/ciphertext pairs
- rotor stepping across candidate positions
- repeated scrambler evaluation at different offsets
- hypothesis checking for plugboard pairings

In its present form, it is closer to a proof-of-concept search tool than a fully polished historical Bombe replica. It captures the core idea of eliminating impossible settings by testing consistent hypotheses, but it does not yet reproduce every detail of the physical Bombe or wartime operational procedure.

## How to run

The project uses the Python standard library and has no external dependencies. Run the files directly with Python:

```bash
python enigma.py
python bombe.py
```

The scripts currently use example values hardcoded near the bottom of each file, so they can be run immediately without entering input. The Bombe example uses the plaintext/ciphertext pair configured in `bombe.py`.

## Project status

What already works:

- Enigma encryption logic
- rotor and reflector wiring tables
- plugboard handling
- Bombe-style menu generation
- candidate rotor-position search

The code also includes console output for tracing rotor positions, turnover checks, scrambler calculations, and Bombe hypotheses.

What is still being worked on:

- turnover handling refinement
- ringstellung support
- post-Bombe plugboard completion
- cleaner input/output handling
- more historically accurate edge-case behavior
- automated tests using known Enigma examples

## Historical notes

This project is historically inspired and educational rather than a claim of complete historical replication. It uses Enigma I wiring data and a Bombe-style search workflow, but the implementation is still a software model rather than a physical machine simulation. In particular, the current implementation should be treated as work in progress until stepping, ring settings, and Bombe plugboard recovery have been validated against authoritative reference examples.

## Known limitations

- Example messages and machine settings are hardcoded instead of supplied through a command-line interface.
- Ringstellung is not yet applied to the rotor signal path.
- Rotor turnover and double-stepping behavior still need further validation.
- The Bombe search does not yet finish the complete plugboard reconstruction automatically.
- Debug output is mixed with normal program output and is not currently configurable.

## Contributing ideas

Useful improvements should preserve the separation between machine simulation and Bombe analysis. Good first contributions include adding a configurable machine setup, writing round-trip and reference-vector tests, and documenting the expected behavior of each rotor and stepping state.

## Notes

- The current code is intentionally exploratory and heavily prints internal state for debugging.
- If you are comparing outputs against a historical Enigma simulator, be aware that small details such as stepping and turnover logic can change results significantly.
