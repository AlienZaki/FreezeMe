from twocaptcha import TwoCaptcha
from twocaptcha.api import ApiException
from core.models import Settings


class CaptchaSolver:

    def __init__(self):
        api_key = Settings.objects.first().captcha_key
        #api_key = '33ca5f964f70eda0c6f94241150e33e9'
        self.solver = TwoCaptcha(api_key)

    def solve_recaptcha(self, site_key, url):
        try:
            print('=> Solving captcha...')
            result = self.solver.recaptcha(sitekey=site_key, url=url)
            print('=> Captcha solved!')
        except ApiException as e:
            errors = {
                'ERROR_BAD_PARAMETERS': '2Captcha: Please check the API key permissions',
                'ERROR_WRONG_USER_KEY': '2Captcha: Invalid Key',
                'ERROR_CAPTCHA_UNSOLVABLE': '2Captcha: Invalid site URL',
                'ERROR_WRONG_GOOGLEKEY': '2Captcha: Wrong google site key',
            }
            raise Exception(errors[e.__str__()])
        return result


if __name__ == '__main__':
    CaptchaSolver()