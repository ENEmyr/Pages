import math
from time import time
from sqlalchemy.orm import Session
from typing import Tuple

import controllers.user as user_controller

AFFINITIES = {'author': 1, 'guest': 2, 'user': 3}
WEIGHTS = {'view': 1, 'fav': 2, 'comment': 3}
USER_POPULARITY_INCREMENT = 5

class PRank:
    '''
    PRank(Original from EdgeRank)
    Used for measure the popularity on page
    By given: Rank(User) = Sum( Popularity(pages) ) + UserPopularity
    Popularity(page) = Ue * We * Gte
    e = every event that occurs to the page such as favorite button cliked, comment or view
    Ue = User affinity to that event that affect to the page popularity, such as User has more affinity than guest or author
    We = Weight of event, different event have a differnt weight, such as weight of view event is less than comment event
    Gte = Page growth trend, that depend on the release time of page the more time passed is mean the more values
          equal to [(ue * we)^(ln (currentTimestamp / ReleaseTimestamp))]
    UserPopularity = User's popularity increase when user got a new follower, whereas decrease when user lost their follower
    In summerized:
                    Rank(User) = Sum( Ue*We*[(ue * we)^(ln (currentTimestamp / ReleaseTimestamp))] ) + UserPopularity
    '''

    def __init__(self, db:Session) -> None:
        self.db = db

    def cal_popularity(self, affinity:str, weight:str, release_time:int) -> int:
        '''
        Calculate popularity
        Affinity set = {'author', 'guest', 'user'}
        Weight set = {'view', 'fav', 'comment'}
        '''
        curr_t = int(time())
        ue = AFFINITIES[affinity]
        we = WEIGHTS[weight]
        if ue != None and we != None and release_time <= curr_t:
            if ue == 0:
                return 0
            gte = (ue*we)**(math.log(curr_t//release_time))
            popularity = ue*we*gte
            return popularity
        else:
            raise ValueError()

    def update_popularity(self, page_id:int, popularity:int) -> Tuple[int, None]:
        '''
        Update page popularity from incomming popularity
        '''
        page = user_controller.get_user(self.db, page_id) # need to replace with page_controller
        try:
            page.rank += int(popularity)
        except Exception as e:
            print(e)
            self.db.rollback()
            return None
        else:
            self.db.commit()
            self.db.refresh(page)
            return page.rank


    def update_rank(self, author_id:int, popularity:float) -> Tuple[int, None]: # can be use `tuple[bool, None]` in python version 3.9+
        '''
        Update author rank from incomming popularity
        '''
        author = user_controller.get_user(self.db, author_id)
        try:
            author.rank += int(popularity)
        except Exception as e:
            print(e)
            self.db.rollback()
            return None
        else:
            self.db.commit()
            self.db.refresh(author)
            return author.rank

    def update_rank_from_follower(self, author_id:int, lost_follower:bool = False) -> Tuple[int, None]:
        '''
        Update author's rank when author got a new follower
        '''
        return self.update_rank(author_id, USER_POPULARITY_INCREMENT if not lost_follower else -USER_POPULARITY_INCREMENT)

    def rank(self, author_id:int) -> int:
        author = user_controller.get_user(self.db, author_id)
        return author.rank if author else 0

    def popularity(self, page_id:int) -> int:
        pass
