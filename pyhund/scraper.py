# [PyHund:Scraper]

import re

from requests import get

from pyhund import SITE_METADATA

class ScraperInstance:

    def __init__(self, site_index: list[str], no_err:bool = False) -> None:
        self.site_index:list[str] = site_index
        self.no_err:bool = no_err

    def list_scan(self, usernames:list[str]) -> None:
        """
        List Scan
        Performs scan for each entry into the list
        """

        for site_name in self.site_index:

            site_data:dict = SITE_METADATA[site_name]

            headers:dict = site_data["headers"] 
            cookies:dict = site_data["cookies"]

            for username in usernames:
                if not username: continue

                site_content = get(site_data["url"].format(username), headers=headers, cookies=cookies)
                if not self.verify(site_name, site_content):
                    if not self.no_err: print(f"[{site_name}:{username}]:: Not Found")
                    continue

                print(f"[{site_name}:{username}]:: {site_data['url'].format(username)}")
    

    def verify(self, site_name:str, site_data:object) -> bool:
        
        meta:dict = SITE_METADATA[site_name]

        if 'verification-method' not in meta:
            return True
        
        match meta['verification-method']:
            case "status":
                return meta['verification-target'] == site_data.status_code
            case "url":
                return meta['verification-target'] in site_data.url
            case "match":
                return not re.search(meta['verification-target'], site_data.text) is None
            case _:
                return True
    
    def threaded_scan(self, usernames:list[str], n_threads:int = 2) -> None:
        return NotImplemented
