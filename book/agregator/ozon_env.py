from .service import user_agent



accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
accept_encoding = 'gzip, deflate, br'
sec_ch_ua_mobile = '?0'
sec_ch_ua_platform = "Linux"
sec_fetch_dest = 'document'
sec_fetch_mode = 'navigate'
sec_fetch_site = 'same-origin'
cache_control = 'max-age=0'

ozon_headers = {'user-agent':user_agent(),
            'accept':accept,
            'accept-encoding':accept_encoding,
            'sec-ch-ua-mobile':sec_ch_ua_mobile,
            'sec-ch-ua-platform':sec_ch_ua_platform,
            'sec-fetch-dest':sec_fetch_dest,
            'sec-fetch-mode':sec_fetch_mode,
            'sec-fetch-site': sec_fetch_site,
            'cache-control':cache_control
            }