from app.service.reports import birthdays_report, marriage_report, daily_birth_report


def get_job(job_name):
    return {
        'birth': birthdays_report,
        'marriage': marriage_report,
        'daily_birth': daily_birth_report
    }[job_name]
