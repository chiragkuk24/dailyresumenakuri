
from src.client.naukri_client import NaukriLoginClient
from src.client.job_client import NaukriJobClient
from src.utils.resume_profile import build_job_search_queries, extract_experience_years, read_resume_text, extract_resume_keywords, resolve_resume_path
from dotenv import load_dotenv, dotenv_values
from colorama import Fore, Style, init
import os
import time

# Load .env file directly to avoid system env var conflicts
load_dotenv()
env_values = dotenv_values('.env')
username = os.getenv("USERNAME") or env_values.get("USERNAME")
password = os.getenv("PASSWORD") or env_values.get("PASSWORD")

init(autoreset=True)

if __name__ == "__main__":
    print(f"{Fore.CYAN}Using credentials from .env file{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  USERNAME: {username}{Style.RESET_ALL}")
    
    # ---------------------------------------------------------------
    # 1. Create client
    # ---------------------------------------------------------------
    client = NaukriLoginClient(username, password)
    
    # ---------------------------------------------------------------
    # 2. Login with password
    # ---------------------------------------------------------------
    print(f"{Fore.CYAN}Attempting password-based login...{Style.RESET_ALL}")
    client.login()
    print(f"{Fore.GREEN}✓ Login successful!{Style.RESET_ALL}")
    # ---------------------------------------------------------------
    # 2. Resume upload — uploads a new PDF resume to your profile
    # ---------------------------------------------------------------
    resume_path = resolve_resume_path(r"D:\CNH\Naukri\Chirag")
    if resume_path and os.path.exists(resume_path):
        print(f"{Fore.CYAN}Uploading resume from: {resume_path}{Style.RESET_ALL}")
        print(client.update_resume(resume_path))
    else:
        print(f"{Fore.YELLOW}Resume file not found at the requested path.{Style.RESET_ALL}")

    # # ---------------------------------------------------------------
    # # 3. Profile update — update headline and summary independently
    # #    Both fields are optional, pass only what you want to change
    # # ---------------------------------------------------------------
    # print(client.update_profile(
    #     headline="Project Management & Payments Domain Expert | 12+ Years | Delivery, Governance, Stakeholder Management"
    # ))

    # print(client.update_profile(
    #     summary="Experienced project and program management professional with 12+ years leading payments, fintech, and digital transformation initiatives."
    # ))

    # # ---------------------------------------------------------------
    # # 4. Misc — fetch profile ID and form key (mostly for debugging)
    # # ---------------------------------------------------------------
    # # print(client.fetch_profile_id())
    # # print(client.get_form_key2())

    # # ---------------------------------------------------------------
    # # 5. Recommended jobs — fetches personalised job listings
    # #    based on your Naukri profile
    # # ---------------------------------------------------------------
    jc = NaukriJobClient(client)
    # jobs = jc.get_recommended_jobs()

    # print("Fetching recommended jobs...")
       



    
    print("Searching jobs...")
    resume_text = read_resume_text()
    keywords = extract_resume_keywords(resume_text)
    experience = extract_experience_years(resume_text)
    target_queries = build_job_search_queries(keywords, location="Bangalore")

    jobs = []
    for query in target_queries:
        keyword = query.replace(" in Bangalore", "")
        jobs = jc.search_jobs(keyword=keyword, location="Bangalore", experience=experience)
        if jobs:
            print(f"{Fore.GREEN}Found {len(jobs)} jobs for '{keyword}'{Style.RESET_ALL}")
            break

    if not jobs:
        print(f"{Fore.YELLOW}  No jobs found for the current resume-driven profile.{Style.RESET_ALL}")
    else:
        print(f"{Fore.GREEN}Using {len(jobs)} jobs for the current resume-driven profile{Style.RESET_ALL}")

        for job in jobs:
            print(f"\n{Fore.CYAN}{'─'*50}{Style.RESET_ALL}")
            print(f"{Fore.WHITE}  Title   : {Fore.YELLOW}{job.title}")
            print(f"{Fore.WHITE}  Company : {Fore.YELLOW}{job.company}")
            print(f"{Fore.WHITE}  Job ID  : {Fore.YELLOW}{job.job_id}")
            print(f"{Fore.WHITE}  Tags    : {Fore.YELLOW}{job.tags}")

            mandatory = job.tags[:2] if job.tags else []
            optional  = job.tags[2:] if len(job.tags) > 2 else []

            try:
                result = jc.apply_job(job, mandatory_skills=mandatory, optional_skills=optional, source="recommended")

                # Check questionnaire
                job_result = (result.get("jobs") or [{}])[0]
                if job_result.get("questionnaire"):
                    print(f"{Fore.YELLOW}   Skipped — questionnaire required{Style.RESET_ALL}")
                    continue

                print(f"{Fore.GREEN}  ✅ Applied successfully!{Style.RESET_ALL}")

            except Exception as e:
                print(f"{Fore.RED}   Failed: {e}{Style.RESET_ALL}")
            
            time.sleep(3)






    # --------------------------------------------------------------- 
    # 6. scrap the jobs,example
    #     
    # ---------------------------------------------------------------
    # i = 1
    # while True:
    #     job_list = jc.search_jobs("Node.js", location="Hyderabad", experience=1, page=i)
    #     for count, job in enumerate(job_list):
    #         print(count + 1, ":-", job.title, " :- ", job.company)
        
    #     breaker = input("enter anything for next page, q to quit: ")
    #     if breaker.strip().lower() == "q":
    #         break
    #     i += 1