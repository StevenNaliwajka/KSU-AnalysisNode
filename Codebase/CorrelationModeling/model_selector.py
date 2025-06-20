# model_selector.py

def prompt_user_for_training_inputs(df):
    print(f"Columns: {list(df.columns)}")
    input_cols = input("Enter input columns (comma-separated): ").strip().split(",")
    input_cols = [col.strip() for col in input_cols]
    output_col = input("Enter output column: ").strip()
    degree = int(input("Enter polynomial degree: "))
    return input_cols, output_col, degree

def prompt_user_for_model_path():
    return input("Enter path to saved model: ").strip()
