# [PyHund:Scraper]

import re
import threading

from requests import get, ConnectionError

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
        try:
            for site_name in self.site_index:

                site_data:dict = SITE_METADATA[site_name]

                headers:dict = site_data["headers"] 
                cookies:dict = site_data["cookies"]

                for username in usernames:
                    if not username: continue

                    try:
                        site_content = get(site_data["url"].format(username), headers=headers, cookies=cookies)
                    except ConnectionError:
                        print(f"[{site_name}:!!!]:: Bad Connection")
                        continue
                    if not self.verify(site_name, site_content):
                        if not self.no_err: print(f"[{site_name}:{username}]:: Not Found")
                        continue

                    print(f"[{site_name}:{username}]:: {site_data['url'].format(username)}")
        except KeyboardInterrupt:
            print("Terminated")
    

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
        
        if len(usernames) < n_threads:
            self.list_scan(usernames=usernames); return
        
        pivot:int = len(usernames) // n_threads
        spill:int = -1 * (len(usernames) % n_threads)
        
        threads = [
            threading.Thread(target=self.list_scan, args=(usernames[pivot * i:pivot * (i + 1)],))
            for i in range(n_threads - 1)
        ]

        threads.append(threading.Thread(target=self.list_scan, args=(usernames[spill:],)))

        [thread.start() for thread in threads]
        [thread.join() for thread in threads]
