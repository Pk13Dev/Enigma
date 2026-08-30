# Enigma and Bombe Simulator

This project is a Python recreation of two historically important machines:

- the German **Enigma** cipher machine
- the **Bombe**, the codebreaking device associated with Alan Turing and Bletchley Park

The goal of the repository is to model how Enigma encryption works and to explore how a Bombe-style search can help recover machine settings from known plaintext and ciphertext pairs.

## What is in the project

- `enigma.py` contains the Enigma simulator.
- `bombe.py` contains the Bombe-style analysis and search logic.

Both scripts use hardcoded Enigma I rotor, reflector, and entry-wheel wirings that match the service machine used by the German Army and Air Force.

## Enigma simulator

The Enigma script currently demonstrates:

- rotor-based substitution encryption
- reflector-based return path
- plugboard swapping
- rotor stepping and turnover behavior

It is designed to take a plaintext message and produce ciphertext while showing some of the internal machine state in the console.

## Bombe implementation

The Bombe script currently demonstrates:

- menu building from plaintext/ciphertext pairs
- rotor stepping across candidate positions
- repeated scrambler evaluation at different offsets
- hypothesis checking for plugboard pairings

In its present form, it is closer to a proof-of-concept search tool than a fully polished historical Bombe replica, but it captures the core idea of eliminating impossible settings by testing consistent hypotheses.

## How to run

Run the files directly with Python:

```bash
python enigma.py
python bombe.py
```

The scripts currently use example values hardcoded near the bottom of each file, so you can run them immediately without entering input.

## Project status

What already works:

- Enigma encryption logic
- rotor and reflector wiring tables
- plugboard handling
- Bombe-style menu generation
- candidate rotor-position search

What is still being worked on:

- turnover handling refinement
- ringstellung support
- post-Bombe plugboard completion
- cleaner input/output handling
- more historically accurate edge-case behavior

## Historical notes

This project is intended to be historically inspired and educational. It uses an Enigma I rotor set and a Bombe-style search workflow, but the implementation is still a software model rather than a physical machine simulation.

## Notes

- The current code is intentionally exploratory and heavily prints internal state for debugging.
- If you are comparing outputs against a historical Enigma simulator, be aware that small details such as stepping and turnover logic can change results significantly.
