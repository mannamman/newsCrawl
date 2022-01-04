from mongo_test import DBworker

if(__name__ == "__main__"):
    subjects = ["tesla", "snp500", "google"]
    for subject in subjects:
        worker = DBworker(subject)
        print(f"{subject=}")
        worker.test_find_all()
        print("="*30)