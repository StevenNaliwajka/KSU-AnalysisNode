from Codebase.Pathing.get_codebase_folder import get_codebase_folder


def get_ml_bin_folder():
    codebase = get_codebase_folder()
    ml_bin_folder = codebase/"CorrelationModeling"/"MLBinary"
    return ml_bin_folder