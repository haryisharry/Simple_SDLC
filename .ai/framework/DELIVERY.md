# Keep coordination records out of product delivery

Keep `.ai` in the development repository when appropriate so both roles retain planning and evidence history. Exclude it from customer source bundles, application packages, container contents and deployment uploads. Do not delete development records to produce a release. If distributing SimpleSDLC itself, `.ai` is the intentional product; this application-delivery rule does not apply to the framework distribution.

The Manager includes packaging requirements in the release task and plan. The worker implements the target project's exclusions outside `.ai`, builds the artifact, checks its contents and records evidence. `.gitignore` alone cannot remove already tracked files or exclude them from every packaging tool.

## Choose exclusions for the actual build

- For Git-generated source archives, assign `.ai export-ignore` in the repository's `.gitattributes` and verify the archive produced from the intended release commit.
- For container builds, exclude `.ai` in the applicable `.dockerignore`, check all build contexts and COPY paths, and inspect the final image filesystem.
- For language packages, configure that package tool's file allowlist/exclusions and inspect its built artifact.
- For deployment uploads or custom source bundles, use an explicit delivery file list or exclude `.ai` in the actual upload/archive step and inspect the staged output.

These are project-specific implementation choices, not files the Manager writes into an application. Test the chosen path against the real build; a rule's presence is insufficient.

## Read-only artifact check

From the project root, run one of:

```text
python .ai/tools/sdlc.py check-delivery path/to/staged-product
python .ai/tools/sdlc.py check-delivery path/to/product.zip
python .ai/tools/sdlc.py check-delivery path/to/product.tar.gz
```

The helper examines a directory tree or ZIP/TAR member names without extracting files. It fails on a `.ai` path component (case-insensitive), symbolic/hard links or special entries, unsafe archive paths, unreadable entry metadata, unsupported input, and empty artifacts. It does not validate file payload integrity, unpack archives nested inside an artifact, inspect container images, follow linked directories or prove the artifact is a complete/working application. Inspect nested bundles, container images and other formats with the appropriate project tools and record those results separately. A staging-directory check alone does not qualify a later package whose contents differ.

Record the build command, release code identity, artifact path and SHA-256, inspection command/exit status and output in release evidence. Check the actual final delivery artifact, and recheck it after rebuilding or repackaging. Also verify required runtime files are present and the application works without `.ai`. Never infer PASS when the artifact has not been built or inspected.
