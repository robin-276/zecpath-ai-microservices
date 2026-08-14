import json
from ats_engine.bias_reducer import BiasReducer
from ats_engine.ranking_engine import CandidateRanker

def run_live_demo():
    print("--- STARTING ZECPATH ATS LIVE DEMO ---\n")
    
    # 1. Load the demo dataset we just created
    with open('demo_data/ats_demo_batch.json', 'r') as file:
        data = json.load(file)
        
    print(f"Job Scenario: {data['demo_scenario']}")
    print("Evaluating 3 candidates...\n")
    
    reducer = BiasReducer()
    ranker = CandidateRanker()
    processed_candidates = []

    # 2. Process each candidate
    for cand in data['candidates']:
        print(f"Analyzing {cand['name']}...")
        
        # Apply Bias Reduction & Normalization
        word_count = len(cand['resume_snippet'].split())
        matched_keywords = int(word_count * cand['keyword_density'])
        
        # Calculate final score and apply keyword stuffing penalties
        fairness_results = reducer.normalize_score(
            raw_score=cand['raw_score'], 
            text_length=word_count, 
            matched_keywords=matched_keywords
        )
        
        cand['final_score'] = fairness_results['final_normalized_score']
        cand['penalty_applied'] = fairness_results['keyword_stuffing_penalty']
        processed_candidates.append(cand)

    # 3. Rank and Shortlist the candidates
    print("\n--- RANKING COMPLETE ---")
    ranked_list = ranker.process_and_rank(processed_candidates)
    
    # 4. Display the results
    for c in ranked_list:
        print(f"Rank #{c['rank']} | {c['name']} | Score: {c['final_score']} | Zone: {c['zone']}")
        if c['penalty_applied'] > 0:
            print(f"   -> ALERT: Candidate penalized -{c['penalty_applied']} points for keyword stuffing.")

if __name__ == "__main__":
    run_live_demo()