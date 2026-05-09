from zod import ZodSequences

dataset_path = "dataset/mini"

zod = ZodSequences(
    dataset_root=dataset_path,
    version="mini"
)

print("Number of sequences:", len(zod))

# första sekvensen
sequence = zod[0]

print("Sequence info:")
print(sequence.info)

print("Sequence path:")
print(sequence.path)

annotation_path = sequence.path / "annotations" / "object_detection.json"
print("Annotation path:", annotation_path)
print("Annotation exists:", annotation_path.exists())