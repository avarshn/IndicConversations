from transformers import AutoTokenizer, AutoModelForCausalLM, AutoModel

def save_model(model_name, model_arch):
        
    local_dir = "../../models/smollm2_360m_instruct"
    device = "cpu"

    tokenizer = AutoTokenizer.from_pretrained(model_name)

    if model_arch == "decoder":
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map=device
        )
    elif model_arch == "encoder":
        model = AutoModel.from_pretrained(
            model_name,
            device_map=device
        )
    
    # else:
    #     model = AutoModel.from_pretrained(
    #         model_name,
    #         device_map=device
    #     )
    
    # Save locally
    tokenizer.save_pretrained(local_dir)
    model.save_pretrained(local_dir)