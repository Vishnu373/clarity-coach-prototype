

def run_pipeline(pipeline_type):

    if pipeline_type == "analysis":
        from .ae_pipeline import run_ae_pipeline
        return run_ae_pipeline()
    
    elif pipeline_type == "assessment":
        from .mi_pipeline import run_mi_pipeline
        return run_mi_pipeline()