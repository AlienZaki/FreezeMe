from twocaptcha import TwoCaptcha
from core.models import Settings


class CaptchaSolver:

    def __init__(self):
        api_key = Settings.objects.first().captcha_key
        print(api_key)
        self.solver = TwoCaptcha(api_key)

    def solve_recaptcha(self, site_key, url):
        result = self.solver.recaptcha(sitekey=site_key, url=url)
        return result


if __name__ == '__main__':
    CaptchaSolver()