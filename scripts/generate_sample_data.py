"""Generate synthetic hospital readmission dataset."""

from src.data.load_data import RAW_DATA_PATH, generate_synthetic_readmission_data, save_dataset


def main() -> None:
    """Generate and save the sample dataset."""

    df = generate_synthetic_readmission_data(n_samples=2500, seed=42)
    save_dataset(df, RAW_DATA_PATH)
    print(f"Saved {len(df)} rows to {RAW_DATA_PATH}")


if __name__ == "__main__":
    main()
