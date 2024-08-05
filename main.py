# [ Main ]

from sys import exit

from pyhund import SITE_METADATA, parser
from pyhund.scraper import ScraperInstance

if __name__ == '__main__':
    
    args = parser.parse_args()
    scraper = ScraperInstance( 
        site_index=list(SITE_METADATA.keys()),
        no_err=args.no_err 
    )

    if not args.users:
        print("Users must be provided")
        exit()
    
    if args.thread:
        scraper.threaded_scan(
            usernames=args.users.split(','), 
            n_threads=args.thread
        ); exit()
    
    scraper.list_scan(usernames=args.users.split(','))
