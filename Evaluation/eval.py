import subprocess
import os
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

model = AutoModelForSeq2SeqLM.from_pretrained('./final_model')
tokenizer = AutoTokenizer.from_pretrained('./final_model')

tasks = [
    ("Write an R function 'convert_DNA_to_RNA()' that converts a DNA sequence to an RNA sequence.", "ATCG", "AUCG"),
    ("Write an R function 'reverse_complement()' that computes the reverse complement of a DNA sequence.", "ATCG", "CGAT"),
    ("Write an R function 'count_GC_content()' that returns the GC content percentage of a DNA sequence.", "GCGC", "100"),
    ("Write an R function 'count_AT_content()' that returns the AT content percentage of a DNA sequence.", "ATAT", "100"),
    ("Write an R function 'is_valid_DNA()' that checks if a sequence only contains A, T, C, G.", "ATCGX", "FALSE"),
    ("Write an R function 'translate_codon()' that translates a single codon into an amino acid.", "AUG", "M"),
    ("Write an R function 'get_codons()' that splits a DNA sequence into codons (triplets).", "ATGCGT", "ATG,CGT"),
    ("Write an R function 'find_motif()' that finds all start positions of a motif in a DNA sequence.", "GATATATGCATATACTT", "2 4 10"),
    ("Write an R function 'count_nucleotides()' that returns a named vector with counts of A, T, C, G.", "AAGCT", "A:2 T:1 C:1 G:1"),
    ("Write an R function 'transcribe_DNA()' that converts a DNA sequence to mRNA.", "TACG", "UACG"), 
    ("Write an R function 'check_palindrome_DNA()' that checks if a DNA sequence is palindromic.", "GAATTC", "TRUE"),
    ("Write an R function 'remove_invalid_characters()' that removes non-DNA letters.", "ATCBZX", "ATC"),
    ("Write an R function 'generate_random_DNA()' that generates a random DNA sequence of given length.", "5", "5"), 
    ("Write an R function 'replace_T_with_U()' that replaces T with U in a sequence.", "TTT", "UUU"),
    ("Write an R function 'reverse_sequence()' that reverses a sequence.", "ATGC", "CGTA")
    ("Write an R function 'validate_RNA_sequence()' that checks if a sequence only has A, U, C, G.", "AUCG", "TRUE"),
]

k_values = [1, 5, 10, 20]
max_k = max(k_values)

os.makedirs("generated_r_scripts", exist_ok=True)

def generate_code(prompt, max_k):
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids
    outputs = model.generate(
        input_ids,
        do_sample=True,
        top_k=50,
        top_p=0.95,
        num_return_sequences=max_k,
        max_length=512
    )
    return [tokenizer.decode(output, skip_special_tokens=True) for output in outputs]

def run_r_script(code, task_idx, sample_idx, test_input, expected_output, special_check=None):
    script_path = f"generated_r_scripts/task_{task_idx}_sample_{sample_idx}.R"

    if isinstance(test_input, tuple):
        input_call = "', '".join(test_input)
    else:
        input_call = test_input

    full_code = code + f"\n\ncat({get_function_call(code, input_call)})\n"

    with open(script_path, "w") as f:
        f.write(full_code)

    try:
        result = subprocess.run(
            ["Rscript", script_path],
            check=True,
            capture_output=True,
            text=True
        )
        output = result.stdout.strip()

        if special_check == "length":
            return len(output) == int(expected_output)
        else:
            return output == expected_output

    except subprocess.CalledProcessError as e:
        return False

def get_function_call(code, input_value):
    if "convert_DNA_to_RNA" in code:
        return f"convert_DNA_to_RNA('{input_value}')"
    elif "reverse_complement" in code:
        return f"reverse_complement('{input_value}')"
    elif "count_GC_content" in code:
        return f"count_GC_content('{input_value}')"
    elif "count_AT_content" in code:
        return f"count_AT_content('{input_value}')"
    elif "is_valid_DNA" in code:
        return f"is_valid_DNA('{input_value}')"
    elif "translate_codon" in code:
        return f"translate_codon('{input_value}')"
    elif "get_codons" in code:
        return f"get_codons('{input_value}')"
    elif "dna_to_numeric" in code:
        return f"dna_to_numeric('{input_value}')"
    elif "find_motif" in code:
        return f"find_motif('{input_value}')"
    elif "count_nucleotides" in code:
        return f"count_nucleotides('{input_value}')"
    elif "transcribe_DNA" in code:
        return f"transcribe_DNA('{input_value}')"
    elif "calculate_molecular_weight" in code:
        return f"calculate_molecular_weight('{input_value}')"
    elif "check_palindrome_DNA" in code:
        return f"check_palindrome_DNA('{input_value}')"
    elif "remove_invalid_characters" in code:
        return f"remove_invalid_characters('{input_value}')"
    elif "generate_random_DNA" in code:
        return f"generate_random_DNA({input_value})"
    elif "replace_T_with_U" in code:
        return f"replace_T_with_U('{input_value}')"
    elif "calculate_tm" in code:
        return f"calculate_tm('{input_value}')"
    elif "reverse_sequence" in code:
        return f"reverse_sequence('{input_value}')"
    elif "remove_whitespace" in code:
        return f"remove_whitespace('{input_value}')"
    elif "validate_RNA_sequence" in code:
        return f"validate_RNA_sequence('{input_value}')"
    else:
        return f"convert_DNA_to_RNA('{input_value}')"

pass_k_sums = {k: 0 for k in k_values}
task_count = len(tasks)

for task_idx, (prompt, test_input, expected_output) in enumerate(tasks):
    special_check = None
    if "generate_random_DNA" in prompt:
        special_check = "length"

    generated_codes = generate_code(prompt, max_k)

    for k in k_values:
        success = False
        for sample_idx in range(k):
            code = generated_codes[sample_idx]
            if run_r_script(code, task_idx, sample_idx, test_input, expected_output, special_check):
                success = True
                break 
        pass_k = 1 if success else 0
        pass_k_sums[k] += pass_k

for k in k_values:
    avg_pass_k = pass_k_sums[k] / task_count
    print(f"Average pass@{k} = {avg_pass_k:.3f}")