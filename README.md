<a id="readme-top"></a>

<div align="center">
	<h1>Sphere-on-Sphere Glenohumeral Shoulder Model</h1>
	<p>
		Musculoskeletal research model for exploring how glenohumeral joint congruence influences humeral head translations, rotator cuff loading, and dynamic stability using Force-Dependent Kinematics (FDK).
		<br />
		<a href="https://doi.org/10.1016/j.jbiomech.2025.112885"><strong>Published paper (Journal of Biomechanics, 2025)</strong></a>
	</p>
</div>

![sphere-shoulder](https://github.com/user-attachments/assets/39d5fb77-38c7-4efe-b45d-24aeb57bd164)

---

## Table of Contents
1. [About the Project](#about-the-project)
2. [Key Features](#key-features)
3. [Scientific Background](#scientific-background)
4. [Repository Layout](#repository-layout)
5. [Installation & Prerequisites](#installation--prerequisites)
6. [How to Run a Simulation](#how-to-run-a-simulation)
7. [Parameterization](#parameterization)
8. [Output & Post-Processing](#output--post-processing)
9. [Typical Use Cases](#typical-use-cases)
10. [Validation & Interpretation Notes](#validation--interpretation-notes)
11. [Roadmap](#roadmap)
12. [Contributing](#contributing)
13. [Citation](#citation)
14. [License](#license)
15. [Acknowledgments](#acknowledgments)

---

## About the Project
This repository contains an AnyBody Modeling System implementation of a sphere-on-sphere glenohumeral (GH) joint formulation coupled with an FDK (Force-Dependent Kinematics) solution strategy. The approach enables the humeral head to translate relative to the glenoid in response to the balance of muscle, passive, and joint reaction forces—rather than prescribing a fixed center of rotation.

The model was developed to investigate how altering joint congruence (relative radii of the humeral head and glenoid representation) affects:
- Humeral head translations (inferosuperior, anteroposterior)
- Rotator cuff muscle force demands (e.g., supraspinatus, infraspinatus, subscapularis)
- Joint stabilization strategies during abduction task

> NOTE: This README summarizes the published work without reproducing copyrighted figures or verbatim text. Please consult the linked open-access article for full methodological and result details.

## Key Features
- Sphere-on-sphere analytic GH joint geometry with configurable radii (`rh`, `rg`).
- FDK-controlled translational DOFs (2 directions) of the humeral head allowing force-driven gliding.
- Parameterized morphotype inputs to explore anatomical variation (radii, insertion adjustments, offsets).
- Abduction moment arm evaluation utility (`EvaluateAbductionMomentArm.any`, etc.).
- Output scripting for extracting muscle forces, joint translations, and reaction loads.

## Scientific Background
Shoulder stability in vivo at mid-range elevation primarily depends on the coordinated production of rotator cuff forces counteracting destabilizing detloid forces. Reducing congruence (e.g., increasing mismatch between humeral and glenoid radii) can:
1. Increase humeral head translations.
2. Elevate required compressive and balancing muscle forces to maintain centering.
3. Alter directionality of resultant joint reaction vectors.

This model represents the glenohumeral joint as a connecting rod rather than a traditional ball-and-socket. The published simulations reported systematic increases in both humeral head displacement and rotator cuff force magnitudes when congruence decreased—qualitatively matching experimental imaging trends.

<!-- ### Conceptual Diagram (Add Later)
You can add a schematic here (e.g., `docs/fig_concept.png`) illustrating:
`Scapula (fixed glenoid sphere)` ↔ `Humeral head sphere` with: radii, translations (ML / IS / AP), muscle force vectors.

```text
				Superior (+IS)
						^
						|      (Supraspinatus)
	 AP (-) < * > AP (+)
						| 
						v
				Inferior (-IS)
``` -->

## Repository Layout
```
├── GH_2spheres.main.any        # Main entry script (load this in AnyBody)
├── Model/                      # Core model & customization scripts
│   ├── Jnt2spheres.any         # Sphere-on-sphere joint + FDK & passive forces
│   ├── Evaluate*MomentArm*.any # Moment arm evaluation utilities
│   ├── ArmMuscleList.any       # Muscle definitions / groupings
│   ├── BodyModelConfiguration.any
│   ├── ScalingCustom_muscle_insertion.any
│   └── ...
├── Input/                      # Morphotype, STL surface, picked point data
│   ├── InputVariables.any      # User-editable parameters (radii, muscle F0, springs)
│   ├── humerus/, scapula/      # Geometries & point clouds
│   └── dumbbell.stl            # External load example
└── README.md                   # This file
```

## Installation & Prerequisites
### Requirements
- AnyBody Modeling System (version supporting FDK constraints; AMS 7.x or later recommended).
- (Optional) Python (for any pre-processing sphere fitting scripts referenced by comments).

### Getting the Model
Clone or download the repository into your AnyBody workspace directory.

```powershell
git clone https://github.com/AnyBody/sphere-on-sphere_shoulder_model.git
```

### Opening in AnyBody
1. Start AnyBody Modeling System.
2. Open `GH_2spheres.main.any`.
3. Adjust parameters in `Input/InputVariables.any` as needed.
4. Load the model to compile kinematics and muscle architecture.

## How to Run a Simulation
1. Open `GH_2spheres.main.any`.
2. (Optional) Select a study (e.g., abduction) if multiple are defined.
3. Run: Kinematics → Inverse Dynamics (FDK will iterate internally on allowed DOFs).
4. Export desired outputs via `AnyOutputFile.any` or add custom `AnyOutputFile` statements.

### Evaluating Moment Arms
Scripts such as `EvaluateAbductionMomentArm.any` can be included or loaded after the main file to compute functional muscle moment arm in specific planes.

## Parameterization
Central user-editable inputs live in `Input/InputVariables.any`.

### MorphotypeParameters
| Parameter | Description | Example Default |
|-----------|-------------|-----------------|
| `rh` | Humeral head sphere radius (m) | 0.0236 |
| `rg` | Glenoid sphere radius (m) | 0.0316 |
| `glenoid_offset` | Translational offset of glenoid sphere center `{x,y,z}` | `{0,0,0}` |
| `CoordoSubscap12/34/56` | Adjusted insertion coordinates for subscapularis fiber sets | (dataset) |
| `AcromionScalingFactor` | Local adjustment for acromial geometry | 0.0 |
| `SupraHumScalingFactor` | Local humeral head adjustment impacting supraspinatus path | 0.0 |

### MusclesPersonalization
`F0<Muscle><FiberIndex>` parameters define maximal isometric force (N) for distinct fiber bundles (deltoid anterior/lateral/posterior, supraspinatus, subscapularis, infraspinatus). Modify to reflect subject-specific strength or scaling experiments.

### FDK Passive Elastic Terms
| Parameter | Axis (Scapular Frame) | Interpretation |
|-----------|-----------------------|----------------|
| `kML` | Mediolateral | Linear spring resisting medial (+) / lateral (−) translation |
| `kIS` | Inferosuperior | Spring resisting superior (+) / inferior (−) glide |
| `kAP` | Anteroposterior | Spring resisting anterior (+) / posterior (−) translation |

Set to zero for unconstrained translational compliance (muscles + joint contact only) or tune to approximate passive capsuloligamentous restraint curves (future enhancement: nonlinear polynomial—commented in `Jnt2spheres.any`).

### Joint Mechanics (`Model/Jnt2spheres.any`)
Key constructs:
- `AnyKinEqSimpleDriver GH_contact`: maintains constant center separation = `rg - rh` (geometric congruence constraint).
- `AnyKinLinear GHLin`: measures 3D vector between sphere centers.
- `GH_fdk`: FDK driver enabling force-dependent solution for two translational components (`MeasureOrganizer = {1,2}`) while constraining distance.

## Output & Post-Processing
Add or modify `AnyOutputFile` blocks (see `Model/AnyOutputFile.any` if present) to extract:
- Muscle forces per time step (`Fm`)
- Joint reaction forces and moments
- Humeral head translation (`GHLin.Pos`) in scapular frame

Example snippet (conceptual):
```anyscript
AnyOutputFile GHTranslations = {
	FileName = "results/GH_translations.txt";
	AnyFloat ML = Main.HumanModel.BodyModel.Right.ShoulderArm.Jnt.GHLin.Pos[0];
	AnyFloat IS = Main.HumanModel.BodyModel.Right.ShoulderArm.Jnt.GHLin.Pos[1];
	AnyFloat AP = Main.HumanModel.BodyModel.Right.ShoulderArm.Jnt.GHLin.Pos[2];
};
```

For batch studies (e.g., sweeping `rg`/`rh` ratios), create a Python or AnyScript macro that edits `InputVariables.any` and relaunches analyses.

## Typical Use Cases
- Sensitivity analysis of joint congruence on muscle force requirements.
- Investigating rotator cuff compensation strategies under altered passive stiffness.
- Educational visualization of GH joint translation under load.
- Preclinical exploration of implant geometry simplifications (sphere-on-sphere prototypes).

## Validation & Interpretation Notes
- Ensure radii values remain within anatomical plausibility (consult imaging-based morphometric studies).
- Excessive humeral head translation may signal insufficient stiffness or unrealistic muscle strength scaling.
- Comparisons to in vivo fluoroscopy or dynamic MRI should consider coordinate frame alignment (scapular reference).
- Passive restraint currently modeled as linear; nonlinear capsular behavior can be reintroduced (commented polynomial in code).

## Roadmap
- [ ] Add nonlinear passive restraint option (restore polynomial terms).
- [ ] Provide automated batch script for congruence sweeps.
- [ ] Add validation dataset & reference kinematic envelopes.
- [ ] Include example post-processing Jupyter notebook (plots: translation vs elevation, cuff force profiles).
- [ ] Add images/diagrams from open-access components of the publication (with proper attribution) or recreated schematics.
- [ ] Parameter documentation auto-generation.

## Contributing
Contributions are welcome:
1. Fork the repo
2. Create a feature branch (`git checkout -b feature/YourFeature`)
3. Commit changes (`git commit -m "feat: add X"`)
4. Push (`git push origin feature/YourFeature`)
5. Open a Pull Request

Please open issues for: bugs, documentation gaps, feature proposals, validation data suggestions.

## Citation
If you use this model, cite the associated paper:

Peixoto M, Soyeux D, Tétreault P, Begon M, Hagemeister N. Effect of congruence variations on a musculoskeletal model considering humeral head displacements. Journal of Biomechanics. 2025;190:112885. doi:10.1016/j.jbiomech.2025.112885

BibTeX:
```bibtex
@article{Peixoto2025SphereOnSphereGH,
	title   = {Effect of congruence variations on a musculoskeletal model considering humeral head displacements},
	author  = {Peixoto, M. and Soyeux, D. and T{\'e}treault, P. and Begon, M. and Hagemeister, N.},
	journal = {Journal of Biomechanics},
	year    = {2025},
	volume  = {190},
	pages   = {112885},
	doi     = {10.1016/j.jbiomech.2025.112885}
}
```

## License
Refer to the repository's license (add a `LICENSE` file if absent). If the intention is open academic reuse, consider a permissive license (e.g., MIT, Apache-2.0) or Creative Commons for data-only content. The linked paper is released under a Creative Commons BY-NC 4.0 license (non-commercial) which does NOT automatically apply to this code unless explicitly stated.

## Acknowledgments
- Original research team (see publication authors).
- AnyBody Technology for the modeling framework.
- Prior morphometric and statistical shape modeling studies informing radii defaults.

## Adding Figures
To enrich this README:
1. Create a `docs/` folder.
2. Add schematic images you have rights to (e.g., recreated diagrams or open-access figures with attribution).
3. Reference them with standard Markdown:
	 `![Conceptual GH Joint](docs/gh_joint_concept.png)`

> Avoid embedding copyrighted publisher figures directly unless license terms allow redistribution in repository form.

---
<p align="right">(<a href="#readme-top">back to top</a>)</p>

