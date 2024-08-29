from bs4 import BeautifulSoup
import requests
import time
import json
import logging

def send_to_telegram(bot_token, chat_id, text):
    url = f"https://api.telegram.org/bot6702100657:AAHib2mUUrsg9GghbV6Pec58p3vi-E2wpLc/sendMessage"
    params = {
        'chat_id': 000000,
        'text': text
    }
    response = requests.post(url, params=params)
    return response.json()

def find_jobs(bot_token, chat_id, previous_jobs):
    html_text = requests.get('https://etcareers.com/jobs/').text
    soup = BeautifulSoup(html_text, 'lxml')
    jobs = soup.find_all('article', class_='media well listing-item listing-item__jobs listing-item__featured')

    for job in jobs:
        job_title = job.find('div', class_='media-heading listing-item__title').text
        job_url = job.div.a.get('href')

        # Check if the job is new based on the unique identifier (job URL)
        if job_url not in [prev_job['url'] for prev_job in previous_jobs]:
            published_date = job.find('div', class_='listing-item__date').text.replace(' ', '')
            desc = ' '.join(job.find('div', class_='listing-item__desc').text.replace('\n', ' ').split())
            more_info = job_url

            message = f"New Job Title: {job_title.strip()} \nJob Description: {desc.strip()} \nPublished On: {published_date.strip()} \nMore info:{more_info}"
            send_to_telegram(bot_token, chat_id, message)

            # Add the new job to the previous_jobs list
            previous_jobs.append({'title': job_title, 'url': job_url})

    return previous_jobs  # Return the updated previous_jobs list

if __name__ == '__main__':
    bot_token = "replace with your bot token"
    chat_id = "0000000"

    # At the start of the script, load previous_jobs from a file
    try:
        with open('previous_jobs.json', 'r') as f:
            previous_jobs = json.load(f)
    except FileNotFoundError:
        previous_jobs = []

    while True:
        previous_jobs = find_jobs(bot_token, chat_id, previous_jobs)
        time_wait = 10
        logging.info(f'Waiting {time_wait} minutes... ')
        time.sleep(time_wait * 60)

        # At the end of the script, save previous_jobs to a file
        with open('previous_jobs.json', 'w') as f:
            json.dump(previous_jobs, f)
