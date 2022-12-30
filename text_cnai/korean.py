# coding: utf-8
# Code based on 

from audioop import reverse
from cgi import test
import re
import os
import ast
import json
from tkinter.font import NORMAL
from jamo import hangul_to_jamo, h2j, j2h
from hangul_utils import split_syllables, join_jamos
# import hanja
from g2pk import G2p
g2p = G2p()

from .smart_g2p.trans import sentranslit as trans



# from .ko_dictionary import english_dictionary, etc_dictionary

# coding: utf-8



etc_dictionary = {
        '2 30대': '이삼십대',
        '20~30대': '이삼십대',
        '20, 30대': '이십대 삼십대',
        '1+1': '원플러스원',
        '3에서 6개월인': '3개월에서 육개월인',
}

chinese_dictionary = {
        '年': '년',
        '月': '월',
        '日': '일',
        '外': '외',
        '內': '내',
        '一': '일',
        '二': '이',
        '三': '삼',
        '四': '사',
        '五': '오',
        '六': '육',
        '七': '칠',
        '八': '팔',
        '九': '구',
        '十': '십',
        '百': '백',
        '千': '천',
        '萬': '만',
        '韓': '한',
        '中': '중',
        '美': '미',
        '英': '영',
        '獨': '독',
        '間': '간',
        '案': '안',
        '必': '필',
        '正': '정',
        '女': '녀',
        '男': '남',
        '東': '동',
        '西': '서',
        '南': '남',
        '北': '북',
        '文': '문',
        '尹': '윤',
        '上': '상',
        '下': '하',
        '左': '좌',
        '右': '우',
        '株': '주'
}

english_dictionary = {
        'Devsisters': '데브시스터즈',
        'track': '트랙',

        # krbook
        'LA': '엘에이',
        'LG': '엘지',
        'KOREA': '코리아',
        'JSA': '제이에스에이',
        'PGA': '피지에이',
        'GA': '지에이',
        'idol': '아이돌',
        'KTX': '케이티엑스',
        'AC': '에이씨',
        'DVD': '디비디',
        'US': '유에스',
        'CNN': '씨엔엔',
        'LPGA': '엘피지에이',
        'P': '피',
        'L': '엘',
        'T': '티',
        'B': '비',
        'C': '씨',
        'BIFF': '비아이에프에프',
        'GV': '지비',

        # JTBC
        'IT': '아이티',
        'IQ': '아이큐',
        'JTBC': '제이티비씨',
        'trickle down effect': '트리클 다운 이펙트',
        'trickle up effect': '트리클 업 이펙트',
        'down': '다운',
        'up': '업',
        'FCK': '에프씨케이',
        'AP': '에이피',
        'WHERETHEWILDTHINGSARE': '',
        'Rashomon Effect': '',
        'O': '오',
        'OO': '오오',
        'B': '비',
        'GDP': '지디피',
        'CIPA': '씨아이피에이',
        'YS': '와이에스',
        'Y': '와이',
        'S': '에스',
        'JTBC': '제이티비씨',
        'PC': '피씨',
        'bill': '빌',
        'Halmuny': '하모니', #####
        'X': '엑스',
        'SNS': '에스엔에스',
        'ability': '어빌리티',
        'shy': '',
        'CCTV': '씨씨티비',
        'IT': '아이티',
        'the tenth man': '더 텐쓰 맨', ####
        'L': '엘',
        'PC': '피씨',
        'YSDJJPMB': '', ########
        'Content Attitude Timing': '컨텐트 애티튜드 타이밍',
        'CAT': '캣',
        'IS': '아이에스',
        'SNS': '에스엔에스',
        'K': '케이',
        'Y': '와이',
        'KDI': '케이디아이',
        'DOC': '디오씨',
        'CIA': '씨아이에이',
        'PBS': '피비에스',
        'D': '디',
        'PPropertyPositionPowerPrisonP'
        'S': '에스',
        'francisco': '프란시스코',
        'I': '아이',
        'III': '아이아이', ######
        'No joke': '노 조크',
        'BBK': '비비케이',
        'LA': '엘에이',
        'Don': '',
        't worry be happy': ' 워리 비 해피',
        'NO': '엔오', #####
        'it was our sky': '잇 워즈 아워 스카이',
        'it is our sky': '잇 이즈 아워 스카이', ####
        'NEIS': '엔이아이에스', #####
        'IMF': '아이엠에프',
        'apology': '어폴로지',
        'humble': '험블',
        'M': '엠',
        'Nowhere Man': '노웨어 맨',
        'The Tenth Man': '더 텐쓰 맨',
        'PBS': '피비에스',
        'BBC': '비비씨',
        'MRJ': '엠알제이',
        'CCTV': '씨씨티비',
        'Pick me up': '픽 미 업',
        'DNA': '디엔에이',
        'UN': '유엔',
        'STOP': '스탑', #####
        'PRESS': '프레스', #####
        'not to be': '낫 투비',
        'Denial': '디나이얼',
        'G': '지',
        'IMF': '아이엠에프',
        'GDP': '지디피',
        'JTBC': '제이티비씨',
        'Time flies like an arrow': '타임 플라이즈 라이크 언 애로우',
        'DDT': '디디티',
        'AI': '에이아이',
        'Z': '제트',
        'OECD': '오이씨디',
        'N': '앤',
        'A': '에이',
        'MB': '엠비',
        'EH': '이에이치',
        'IS': '아이에스',
        'TV': '티비',
        'MIT': '엠아이티',
        'KBO': '케이비오',
        'I love America': '아이 러브 아메리카',
        'SF': '에스에프',
        'Q': '큐',
        'KFX': '케이에프엑스',
        'PM': '피엠',
        'Prime Minister': '프라임 미니스터',
        'Swordline': '스워드라인',
        'TBS': '티비에스',
        'DDT': '디디티',
        'CS': '씨에스',
        'Reflecting Absence': '리플렉팅 앱센스',
        'PBS': '피비에스',
        'Drum being beaten by everyone': '드럼 빙 비튼 바이 에브리원',
        'negative pressure': '네거티브 프레셔',
        'F': '에프',
        'KIA': '기아',
        'FTA': '에프티에이',
        'Que sais-je': '',
        'UFC': '유에프씨',
        'P': '피',
        'DJ': '디제이',
        'Chaebol': '채벌',
        'BBC': '비비씨',
        'OECD': '오이씨디',
        'BC': '삐씨',
        'C': '씨',
        'B': '씨',
        'KY': '케이와이',
        'K': '케이',
        'CEO': '씨이오',
        'YH': '와이에치',
        'IS': '아이에스',
        'who are you': '후 얼 유',
        'Y': '와이',
        'The Devils Advocate': '더 데빌즈 어드보카트',
        'YS': '와이에스',
        'so sorry': '쏘 쏘리',
        'Santa': '산타',
        'Big Endian': '빅 엔디안',
        'Small Endian': '스몰 엔디안',
        'Oh Captain My Captain': '오 캡틴 마이 캡틴',
        'AIB': '에이아이비',
        'K': '케이',
        'PBS': '피비에스'
}

PAD = '_'
EOS = '~'
PUNC = '!\'(),-.:;?'
SPACE = ' '

JAMO_LEADS = "".join([chr(_) for _ in range(0x1100, 0x1113)])
JAMO_VOWELS = "".join([chr(_) for _ in range(0x1161, 0x1176)])
JAMO_TAILS = "".join([chr(_) for _ in range(0x11A8, 0x11C3)])

VALID_CHARS = JAMO_LEADS + JAMO_VOWELS + JAMO_TAILS + PUNC + SPACE
ALL_SYMBOLS = PAD + EOS + VALID_CHARS

char_to_id = {c: i for i, c in enumerate(ALL_SYMBOLS)}
id_to_char = {i: c for i, c in enumerate(ALL_SYMBOLS)}

quote_checker = """([`"'＂“‘])(.+?)([`"'＂”’])"""

def is_lead(char):
    return char in JAMO_LEADS

def is_vowel(char):
    return char in JAMO_VOWELS

def is_tail(char):
    return char in JAMO_TAILS

def get_mode(char):
    if is_lead(char):
        return 0
    elif is_vowel(char):
        return 1
    elif is_tail(char):
        return 2
    else:
        return -1

def _get_text_from_candidates(candidates):
    if len(candidates) == 0:
        return ""
    elif len(candidates) == 1:
        return _jamo_char_to_hcj(candidates[0])
    else:
        return j2h(**dict(zip(["lead", "vowel", "tail"], candidates)))

def jamo_to_korean(text):
    text = h2j(text)

    idx = 0
    new_text = ""
    candidates = []

    while True:
        if idx >= len(text):
            new_text += _get_text_from_candidates(candidates)
            break

        char = text[idx]
        mode = get_mode(char)

        if mode == 0:
            new_text += _get_text_from_candidates(candidates)
            candidates = [char]
        elif mode == -1:
            new_text += _get_text_from_candidates(candidates)
            new_text += char
            candidates = []
        else:
            candidates.append(char)

        idx += 1
    return new_text

english_dictionary_new = {
        'abcp': '에이비씨피', 
        'abuse': '엠뷰즈', 
        'accepted': '어셉티드', 
        'accident': '엑시던트', 
        'account': '어카운트', 
        'accountants': '어카운턴스', 
        'accounting': '어카운팅', 
        'acquisition': '어퀴시젼', 
        'acquisitions': '애퀴지션즈', 
        'acqusition': '애퀴지션', 
        'act': '앸트', 
        'acted': '액티드', 
        'action': '액션', 
        'active': '액티브', 
        'activities': '엑티비티스', 
        'acts': '앸츠', 
        'actuary': '액츄어리', 
        'adb': '에이디비', 
        'added': '애디드', 
        'adequacy': '애디쿼시', 
        'adjuster': '어드져스터', 
        'administration': '어드미니스트레이션', 
        'administrative': '어니미니스트레이티브', 
        'advanced': '어드벤스드', 
        'adverse': '어드벌스', 
        'adviser': '어드바이져', 
        'advisor': '어드바이져', 
        'advisory': '어드바이저리', 
        'affiliate': '어필리에이트', 
        'afir': '에이에프아이알', 
        'after': '애프터', 
        'against': '어게인스트', 
        'agency': '에이전시', 
        'agent': '에이전트', 
        'agreement': '어그리먼트', 
        'aiib': '에이아이아이비', 
        'algorithm': '알고리즘', 
        'allocation': '얼로케이션', 
        'alm': '에이엘엠', 
        'alone': '얼론', 
        'aml': '에이엠엘', 
        'amount': '어마운트', 
        'amro': '에이엠알오', 
        'an': '언', 
        'analysis': '애널리시스', 
        'and': '엔드', 
        'anti': '안티', 
        'apec': '에이피이씨', 
        'api': '에이피아이', 
        'application': '애플리케이션', 
        'appointed': '어포인티드', 
        'appointment': '어우디팅', 
        'appraisal': '앺레이셜', 
        'approach': '어프로치', 
        'approval': '어프루벌', 
        'apt': '에이피티', 
        'asean': '에이에스이에이엔', 
        'asian': '아시안', 
        'assessment': '에세스멘트', 
        'asset': '에셋', 
        'assets': '에셋츠', 
        'association': '어소시에이션', 
        'assurance': '어슈어런스', 
        'at': '엣', 
        'audit': '어우딧', 
        'auditing': '어우디팅', 
        'auditor': '어우디털', 
        'auto': '오토', 
        'automatic': '오토매틱', 
        'available': '어베일러블', 
        'ba': '비에이', 
        'back': '백', 
        'backed': '백드', 
        'backwardation': '백워데이션', 
        'balance': '밸런스', 
        'bancassurance': '반카슈어랜스', 
        'bank': '뱅크', 
        'banking': '뱅킹', 
        'banks': '벵크스', 
        'base': '베이스', 
        'based': '베이스드', 
        'basic': '베이직', 
        'bcbs': '비씨비에스', 
        'bcp': '비씨피', 
        'before': '비포어', 
        'beneficiaries’': '베네피셔라이즈', 
        'benefit': '베네핏', 
        'beyond': '비욘드', 
        'bias': '바이아스', 
        'bid': '비드', 
        'bis': '비아이에스', 
        'black': '블랙', 
        'block': '블록', 
        'blockchain': '북체인', 
        'bmbenchmark': '비엠벤치마크', 
        'board': '보드', 
        'bok': '비오케이', 
        'bond': '본드', 
        'book': '북', 
        'bop': '비오피', 
        'border': '볼더', 
        'borrowing': '버로윙', 
        'breakers': '브레이커스', 
        'brexit': '브렉싵', 
        'broker': '브로커', 
        'brokerage': '브로커레이지', 
        'bsi': '비에스아이', 
        'buffer': '버퍼', 
        'building': '빌딩', 
        'bureau': '뷰어로', 
        'business': '비즈니스', 
        'but': '벋', 
        'buyer': '바이어', 
        'bw': '비떠블유', 
        'by': '바이', 
        'c&c': '씨앤씨', 
        'cacrel': '씨에이씨알이엘', 
        'call': '콜', 
        'camel': '카멜', 
        'capital': '캐피탈', 
        'capitalism': '캐피탈리즘', 
        'captial': '캐피털', 
        'card': '카드', 
        'cardholder': '카드홀더', 
        'carry': '캐리', 
        'cash': '캐쉬', 
        'cb': '씨비', 
        'ccyb': '씨씨와이비', 
        'cd': '씨디', 
        'cdo': '씨디오', 
        'ceiling': '실링', 
        'center': '센터', 
        'central': '센트럴', 
        'certified': '썰티파이드', 
        'cfc': '씨에프씨', 
        'cfp': '씨에프피', 
        'chief': '치프', 
        'chinese': '차이니즈', 
        'churning': '쳐닝', 
        'circuit': '써킷', 
        'ciso': '씨아이에스오', 
        'claims': '클레임즈', 
        'classified': '클래시파이드', 
        'cln': '씨엘엔', 
        'cloud': '클라우드', 
        'cls': '씨엘에스', 
        'cma': '씨엠에이', 
        'cmi': '씨엠아이', 
        'cmo': '씨엠오', 
        'cms': '씨엠에스', 
        'code': '코드', 
        'cofix': '코픽스', 
        'coin': '코인', 
        'collateral': '콜러터럴', 
        'collection': '컬렉션', 
        'college': '컬리지',
        'bio': '바이오',
        'amundi':'아문디', 
        'comframe': '컴프레임', 
        'command': '커멘트', 
        'commercial': '커머셜', 
        'commission': '커미션', 
        'commissions': '커미션즈', 
        'commitment': '커밋멘트', 
        'committee': '커미티', 
        'commodity': '컴머디티', 
        'common': '커먼', 
        'company': '컴퍼니', 
        'compensating': '컴펜세이팅', 
        'compensation': '컴펜세이션', 
        'compliance': '컴플레인스', 
        'comprehensive': '컴프리헨시브', 
        'computing': '컴퓨팅', 
        'conducted': '컨덕티드', 
        'conference': '컨퍼런스', 
        'conservation': '컨절베이션', 
        'consolidated': '컨솔리데이티드', 
        'consumer': '컨슈머', 
        'contact': '콘택트', 
        'contango': '콘탱고', 
        'contingency': '컨틴전시', 
        'continuity': '컨티뉴이티', 
        'contract': '컨트렉트', 
        'contribution': '컨트리뷰션', 
        'control': '컨트롤', 
        'conversion': '컨버젼', 
        'cooperative': '쿠퍼레이티브', 
        'core': '코어', 
        'corporate': '쿠퍼레이트', 
        'corporation': '코퍼레이션', 
        'corrective': '커엑티브', 
        'counter': '카운터', 
        'countercyclical': '카운터싸이클리컬', 
        'coverage': '커버리지', 
        'cp': '씨피', 
        'cpi': '씨피아이', 
        'cpmi': '씨피엠아이', 
        'cpo': '씨피오', 
        'credit': '크레딧', 
        'creditor': '크레디터', 
        'crime': '크라임', 
        'criteria': '크라이티어리아', 
        'critical': '크리티컬', 
        'cross': '크로스', 
        'crowd': '크라우드', 
        'csi': '씨에스아이', 
        'currencies': '커렌시스', 
        'currency': '커렌시', 
        'curreny': '커렌시', 
        'customer': '커스터머', 
        'cut': '컷', 
        'cvm': '씨브이엠', 
        'cyclical': '싸이클리컬', 
        'damages': '데미지스', 
        'dart': '다트', 
        'data': '데이터', 
        'day': '데이', 
        'db': '디비', 
        'dc': '디씨', 
        'ddos': '디디오에스', 
        'dealer': '딜러', 
        'debt': '뎊트', 
        'debtor': '뎊터', 
        'debtrank': '뎊트랭크', 
        'deceptive': '디셉티브', 
        'declaration': '디클레어러션', 
        'default': '디폴트', 
        'defined': '디파인드', 
        'deflation': '디플레네이션', 
        'deliberation': '델리버레이션', 
        'delta': '델타', 
        'denial': '디나이얼', 
        'deposit': '디파짇', 
        'depositors': '데포지터스', 
        'depository': '데포지토리', 
        'deposits': '데포짓스', 
        'depth': '뎊스', 
        'derivatives': '더리베이티브즈', 
        'designation': '디자이네이션', 
        'detection': '디텍션', 
        'disaster': '디재스터', 
        'disciplinary': '디서플레네리', 
        'disclosed': '디스클로즈드', 
        'disclosure': '디스클로져', 
        'disclosures': '디스클로져스', 
        'discretionary': '디스트리셔너리', 
        'disgorgement': '디스조지먼트', 
        'dispute': '디스퓨트', 
        'distributed': '디스트리뷰티드', 
        'dividend': '디버덴드', 
        'dls': '디엘에스', 
        'do': '두', 
        'document': '도큐먼트', 
        'dodd': '도드', 
        'dollar': '달러', 
        'domestic': '도메스틱', 
        'door': '도어', 
        'dormant': '도얼먼트', 
        'dr': '디알', 
        'dsr': '디에스알', 
        'dti': '디티아이', 
        'dual': '듀얼', 
        'duty': '듀티', 
        'dvp': '디브이피', 
        'dynamic': '다이내믹', 
        'ead': '이에이디', 
        'early': '이얼리', 
        'earning': '이얼닝', 
        'eb': '이비', 
        'ebrd': '이비알디', 
        'ec': '이씨', 
        'ecb': '이씨비', 
        'education': '에듀케이션', 
        'eft': '이에프티', 
        'eld': '이엘디', 
        'electronic': '일렉트로닉', 
        'els': '이엘에스', 
        'else': '엘스', 
        'elw': '이엘더블유', 
        'embi': '디엠비아이', 
        'emeap': '이엠이에이피', 
        'end': '엔드', 
        'enforcement': '인폴스먼트', 
        'entities': '엔티티스', 
        'entity': '엔티티', 
        'entrustment': '엔트러스트먼트', 
        'environmental': '인바이런멘탈', 
        'eps': '이피에스', 
        'equity': '에퀴티', 
        'equivalence': '이퀴벌런스', 
        'escrow': '에스크로', 
        'estate': '에스테이트', 
        'etf': '이티에프', 
        'eu': '이유', 
        'euribor': '이유알아이비오알', 
        'euro': '유로', 
        'evaluation': '이벨류에이션', 
        'examination': '익재미네이션', 
        'examinations': '익재미네이션즈', 
        'examiners': '익재미널스', 
        'exchange': '익스체인지', 
        'exclusion': '익스클루션', 
        'execution': '익스큐션', 
        'executive': '엑스큐티브', 
        'exercise': '엑서사이즈', 
        'expense': '익스펜스', 
        'expenses': '엑스펜시스', 
        'experienced': '익스피리언스드', 
        'expert': '엑스퍼트', 
        'exposure': '익스포슈어', 
        'exposures': '엑스포셔스', 
        'extensible': '익스텐시블', 
        'external': '익스터널', 
        'face': '페이스', 
        'facilities': '팩실리티스', 
        'factors': '팩터스', 
        'facts': '팩츠', 
        'facultative': '패큘레이티브', 
        'fatf': '에프에이티에프', 
        'fds': '에프디에스', 
        'fdsc': '에프디에스씨', 
        'fee': '피', 
        'feeder': '페더', 
        'fees': '피스', 
        'fi': '에프아이', 
        'finance': '파이낸스', 
        'financial': '파이낸셜', 
        'financing': '파이낸싱', 
        'fintech': '핀테크', 
        'firm': '핆', 
        'five': '파이브', 
        'flow': '플로우', 
        'fn': '에프앤', 
        'for': '포', 
        'force': '포스', 
        'foreign': '포린', 
        'forum': '포럼', 
        'forward': '포워드', 
        'fourth': '폴쓰', 
        'fq': '에프큐', 
        'framework': '프레임워크', 
        'frank': '프랭크', 
        'fraud': '프라우드', 
        'frb': '에프알비', 
        'frn': '에프알엔', 
        'front': '프론트', 
        'frozen': '프로즌', 
        'frs': '에프알에스', 
        'fsb': '에프에스비', 
        'fta': '에프티에이', 
        'ftse': '에프티에스이', 
        'fund': '펀드', 
        'funding': '펀딩', 
        'funds': '펀즈', 
        'futures': '퓨쳐스', 
        'gcf': '지씨피', 
        'gdp': '지디피', 
        'general': '제너럴', 
        'generally': '제네널리', 
        'giro': '지아이알오', 
        'given': '기븐', 
        'global': '글로벌', 
        'governing': '거붤닝', 
        'gray': '그레이', 
        'green': '그린', 
        'greenfield': '그린필드', 
        'group': '그룹', 
        'groups': '그룹스', 
        'guarantee': '개런티', 
        'guaranteed': '게런티드', 
        'guidance': '가이던스', 
        'gvc': '지브이씨', 
        'handy': '핸디', 
        'hard': '하드', 
        'hazard': '해져드', 
        'hdri': '에이치디알아이', 
        'health': '헬스', 
        'hedge': '헤지', 
        'herstatt': '에르스타트', 
        'hhi': '에이치에이치아이', 
        'holder': '홀더', 
        'holding': '홀딩', 
        'hours': '하우얼스', 
        'hub': '허브', 
        'hybrid': '하이브리드', 
        'i/o': '아이/오/', 
        'iais': '아이에이아이에스', 
        'ibnr': '아이비엔알', 
        'ic': '아이씨', 
        'icaap': '아이씨에이에이피', 
        'ico': '아이씨오', 
        'icp': '아이씨피', 
        'identification': '아이덴티피케이션', 
        'ifa': '아이에프에이', 
        'ifas': '아이에프에이에스', 
        'ifiar': '아이에프아이에이알', 
        'ifrs': '아이에프알에스', 
        'ifsc': '아이에프에스씨', 
        'iip': '아이아이피', 
        'illiteracy': '이터레이시', 
        'illness': '일네스', 
        'imf': '아이엠에프', 
        'importance': '임폴턴스', 
        'important': '임폴턴트', 
        'in': '인', 
        'incident': '인시덴트', 
        'inclusion': '인클루션', 
        'income': '인컴', 
        'increase': '인크리스', 
        'incurred': '인큐어드', 
        'indemnity': '인데미니티', 
        'independent': '인디펜던트', 
        'index': '인덱스', 
        'indicator': '인디케이터', 
        'individual': '인디비쥬얼', 
        'industrial': '인더스트리얼', 
        'infe': '아이엔에프이', 
        'information': '인포메이션', 
        'informative': '인포매티브', 
        'infra': '인프라', 
        'initial': '이니셜', 
        'initiative': '이니시에이티브', 
        'inquired': '인콰이얼드', 
        'inquiry': '인쿼리', 
        'insider': '인사이더', 
        'inspection': '인스펙션', 
        'installment': '인스탈멘트', 
        'institute': '인스티튜트', 
        'institution': '인스티튜션', 
        'institutional': '인스시튜셔널', 
        'instruments': '인스트루멘츠', 
        'insurance': '인슈런스', 
        'insurtech': '인슈어테크', 
        'integrated': '인테그레이티드', 
        'interconnectedness': '인터커넥티드네스', 
        'interest': '인터레스트', 
        'internal': '인터널', 
        'international': '인터네셔널', 
        'internationally': '인터네셔널리', 
        'internet': '인터넷', 
        'investigation': '인베스티게이션', 
        'investment': '인베스트먼트', 
        'investor': '인베스터',  
        'iops': '아이오피에스', 
        'iosco': '아이오에스씨오', 
        'ipo': '아이피오', 
        'irb': '아이알비', 
        'irp': '아이알피', 
        'isa': '아이에스에이', 
        'isar': '아이에스에이알', 
        'issues': '이슈스', 
        'it': '아이티', 
        'joint': '조인트', 
        'kai': '케이에이아이', 
        'kam': '케이에이엠', 
        'key': '키', 
        'kicpa': '케이아이씨피에이', 
        'know': '노우', 
        'korea': '코리아', 
        'korean': '코리안', 
        'kospi': '코스피', 
        'kycr': '케이와이씨알', 
        'land': '랜드',
        'kosdaq':'코스닥', 
        'language': '랭귀지', 
        'large': '럴쥐', 
        'lat': '엘에이티', 
        'late': '레이트', 
        'laundering': '라운더링', 
        'lbo': '엘비오', 
        'lead': '리드', 
        'lease': '리즈', 
        'lender': '랜더', 
        'lending': '랜딩', 
        'letter': '레터', 
        'level': '레벨', 
        'leverage': '레버리지', 
        'lgd': '엘쥐디', 
        'liability': '리어빌리티', 
        'life': '라이프', 
        'linked': '링크드', 
        'liquidity': '리퀴디티', 
        'listing': '리스닝', 
        'loan': '로언', 
        'loans': '로언스', 
        'looking': '루킹', 
        'loss': '로스', 
        'lp': '엘피', 
        'ltv': '엘티브이', 
        'madymo': '엠에이디와이엠오', 
        'main': '메인',
        'manage' : '매니지',
        'manager' : '매니저',
        'management': '매니지먼트', 
        'manipulation': '매니퓰레이션', 
        'manual': '매뉴얼', 
        'margin': '마진', 
        'market': '마켓', 
        'master': '마스터', 
        'matched': '매치드', 
        'material': '머테리얼', 
        'materials': '메태리얼스', 
        'mathematical': '메쓰메티컬', 
        'matters': '매터스', 
        'mbs': '엠비에스', 
        'measures': '메졀스', 
        'medical': '메디컬', 
        'meeting': '미팅', 
        'member': '멤벌', 
        'members': '멤버스', 
        'merchant': '멀췐트', 
        'mergers': '멀져스', 
        'method': '메소드', 
        'mezzanine': '매저닌', 
        'minimum': '미니멈', 
        'mmf': '엠엠에프', 
        'models': '모델스', 
        'monetary': '모네터리', 
        'money': '머니', 
        'monitoring': '모니터링', 
        'month': '먼쓰', 
        'moral': '모랄', 
        'moratorium': '모라토리움', 
        'mortgage': '몰기지', 
        'multiclass': '멀티클래스', 
        'mutual': '뮤추얼', 
        'mystery': '미스터리', 
        'nafta': '엔에이에프티에이', 
        'name': '네임', 
        'nations': '네이션즈', 
        'ncr': '엔씨알', 
        'ndf': '엔디에프', 
        'net': '넷', 
        'network': '네트워크', 
        'new': '뉴', 
        'nim': '엔아이엠', 
        'no': '노', 
        'noe': '엔오이', 
        'non': '논', 
        'nonpublic': '논퍼블릭', 
        'not': '낫', 
        'notice': '노티스', 
        'notify': '노티파이', 
        'objection': '오브젝션', 
        'oecd': '오이씨디', 
        'of': '오브', 
        'off': '오프', 
        'offender': '어펜더', 
        'offering': '오퍼링', 
        'officer': '오피서', 
        'offshore': '오프쇼어', 
        'ombudsman': '옴부즈맨', 
        'omnibus': '옴니버스', 
        'fomc':'에프오엠씨',
        'on': '온', 
        'one': '원', 
        'only': '온리', 
        'open': '오픈', 
        'operational': '오퍼레이셔널', 
        'opinions': '오피니언스', 
        'option': '옵션', 
        'or': '오알', 
        'orders': '오더스', 
        'ordinary': '올디너리', 
        'organisation': '올가니제이션', 
        'organization': '올가니제이션', 
        'other': '아더', 
        'otp': '오티피', 
        'outsourcing': '아웃소싱', 
        'outstanding': '아웃스탠딩', 
        'over': '오버', 
        'oversight': '오버싸이트', 
        'own': '오운', 
        'ownership': '오널쉽', 
        'pad': '패드', 
        'paper': '페이퍼', 
        'parties': '파티스', 
        'password': '패스워드', 
        'pca': '피씨에이', 
        'pd': '피디', 
        'peer': '피얼', 
        'pef': '피이에프', 
        'pension': '펜션', 
        'per': '피이알', 
        'percent': '퍼센트', 
        'performance': '퍼포먼스', 
        'performing': '펄포밍', 
        'period': '피리오드', 
        'persistency': '퍼시스텐시', 
        'persistent': '펄시스턴트', 
        'personal': '펄스널', 
        'pf': '피에프', 
        'pharming': '파밍', 
        'phishing': '피싱', 
        'pillar': '필라', 
        'pin': '핀', 
        'placement': '플레이스먼트', 
        'plan': '플랜', 
        'planning': '플래닝', 
        'point': '포인트', 
        'points': '포인츠', 
        'policy': '폴리시', 
        'policyholder': '폴리시홀더', 
        'ponzi': '폰지', 
        'portal': '포탈', 
        'position': '포지션', 
        'positions': '포지션즈', 
        'possessor': '포세설', 
        'ppi': '피피아이', 
        'practical': '프랙티컬', 
        'practices': '프텍티시즈', 
        'pre': '프리', 
        'premium': '프리미엄', 
        'price': '프라이스', 
        'pricing': '프라이싱', 
        'principal': '프린시펄', 
        'principle': '프린시플', 
        'principles': '프린시펄', 
        'prior': '프라이어', 
        'privacy': '프라이버시', 
        'private': '프라이빗', 
        'probability': '프로버빌리티', 
        'proceeds': '프로시드즈', 
        'process': '프로세스', 
        'procyclicality': '프로사이슬리컬리티', 
        'product': '프로덕트', 
        'professional': '프로페셔널', 
        'profit': '프로핏', 
        'program': '프로그램', 
        'programme': '프로그래미', 
        'project': '프로젝트', 
        'promotion': '프로모션', 
        'prompt': '프롬프트', 
        'property': '프로퍼티', 
        'proportional': '프로포셔널', 
        'prospectus': '프로스펙터스', 
        'protection': '프로텍션', 
        'provider': '프로바이더', 
        'proxy': '프록시', 
        'public': '퍼블릭', 
        'purpose': '퍼포즈', 
        'put': '푿', 
        'pvp': '피브이피', 
        'qa': '큐에이', 
        'qib': '큐아이비', 
        'qualified': '퀄리파이드', 
        'quality': '퀄리티', 
        'quasi': '콰지', 
        'quotient': '쿠오션트', 
        'ra': '알에이', 
        'raas': '알에이에이에스', 
        'rams': '알에이엠에스', 
        'ransomware': '랜섬웨어', 
        'rate': '레이트', 
        'rates': '레이츠', 
        'rating': '레이팅', 
        'ratings': '레이팅스', 
        'ratio': '레이시오', 
        'rbc': '알비씨', 
        'rbs': '알비에스', 
        'rca': '알씨에이', 
        'rcsa': '알씨에스에이', 
        'real': '리얼', 
        'receipt': '리싶트', 
        'recommendations': '레커멘데이션스', 
        'recovery': '리커버리', 
        'recurring': '리큐어링', 
        'redemption': '러댐션', 
        'regime': '러짐', 
        'registration': '레지스트레이션', 
        'regtech': '렉테크', 
        'regulation': '레귤레이션', 
        'regulations': '레귤레이션즈', 
        'regulators': '레귤레이터스', 
        'reinsurance': '뤼인슈어런스', 
        'reits': '리츠', 
        'relationship': '릴레이션십', 
        'renewal': '리뉴얼', 
        'replacement': '리플레이스먼트', 
        'repo': '레포', 
        'report': '리포트', 
        'reported': '리포티드', 
        'reporter': '리포터', 
        'reporting': '리포팅', 
        'reports': '리포츠', 
        'repurchase': '리펄쳐스', 
        'request': '리퀘스트', 
        'reserch': '이서피', 
        'reserve': '뤼져브', 
        'resolution': '레절루션', 
        'responsibilities': '리스폰스빌리티스', 
        'restructure': '리스트럭쳐', 
        'restructuring': '리스트럭튜어링', 
        'retention': '리텐션', 
        'retirement': '리타이얼먼트', 
        'retrieval': '리트리벌', 
        'return': '리턴', 
        'reversal': '리버설', 
        'review': '리뷰', 
        'revolution': '레볼루션', 
        'revolving': '리벌빙', 
        'rewarding': '리월딩', 
        'right': '롸잇', 
        'rights': '롸이츠', 
        'risk': '리스크',
        'focus':'포커스',
        'robo': '로보', 
        'roca': '알오씨에이', 
        'rollover': '롤오버', 
        'rp': '알피', 
        'rrp': '알알피', 
        'rule': '룰', 
        'run': '런', 
        'running': '러닝', 
        'rwa': '알더블유에이', 
        'sales': '세일즈', 
        'sanction': '생크션', 
        'savings': '세이빙스', 
        'sb': '에쓰비', 
        'scale': '스케일', 
        'scheme': '스키마', 
        'school': '스쿨', 
        'seacen': '에쓰디에이씨이엔', 
        'secondary': '세컨데리', 
        'securities': '세큐리티즈', 
        'securitization': '세큐리티제이션', 
        'security': '세큐리티', 
        'selection': '셀렉션', 
        'self': '셀프', 
        'seller': '셀러', 
        'selling': '셀링', 
        'separate': '세퍼레이트', 
        'seriiousness': '시리우스니스', 
        'server': '서버', 
        'service': '서비스', 
        'settlement': '세틀먼트', 
        'settlements': '새틀먼츠', 
        'shadow': '쉐도우', 
        'shareholdes': '쉐얼홀더스', 
        'sharing': '쉐어링', 
        'shelf': '쉘프', 
        'shoe': '슈', 
        'shopping': '쇼핑', 
        'shore': '쇼어', 
        'short': '쇼트', 
        'sib': '에스아이비', 
        'sidecar': '사이드카', 
        'sifi': '에스아이에프아이', 
        'site': '싸이트', 
        'smishing': '스미싱', 
        'snasocial': '에스엔에이소셜', 
        'soft': '소프트', 
        'solicitation': '쏠리씨테이션', 
        'solicitor': '솔리시터', 
        'solvency': '솔벤시', 
        'someone': '썸원', 
        'spac': '에스피에이씨', 
        'special': '스페셜', 
        'specialized': '스페셜라이즈드', 
        'specified': '스페시파이드', 
        'split': '스플릿', 
        'stability': '스테이빌리티', 
        'stable': '스테이블', 
        'staff': '스태프', 
        'stage': '스테이지', 
        'stand': '스탠드', 
        'standard': '스탠다드', 
        'standards': '스탠다즈', 
        'standing': '스탠딩', 
        'statement': '스테이트먼트', 
        'statements': '스테이트먼츠', 
        'status': '스테이터스', 
        'stewardship': '스튜어드쉽', 
        'stock': '스톡', 
        'stockholder': '스톡홀더', 
        'stocks': '스톡스', 
        'stress': '스트레스', 
        'strips': '에스티알아이피에스', 
        'st udent': '스튜덴트', 
        'subprime': '서브프라임', 
        'subscription': '섭스크립션', 
        'subsidiary': '섭시디에리', 
        'substitutabilit y': '섭스터튜터빌리티', 
        'suitability': '수터빌리티', 
        'supervision': '슈퍼바이젼', 
        'supervisors': '슈퍼바이져스', 
        'surren der': '서렌더', 
        'sut': '에쓰유티', 
        'swan': '스완', 
        'swap': '스왑', 
        'swing': '스윙', 
        'switching': '스위칭', 
        'synthetic': '신태틱', 
        'system': '시스템', 
        'systemic': '시스테믹', 
        'systemically': '시스테미컬리', 
        'tables': '테이블즈', 
        'take': '테이크', 
        'taken': '테이큰', 
        'tapering': '테이퍼링', 
        'target': '탈겟', 
        'task': '테스크', 
        'tax': '텍스', 
        'technology': '테크놀러지', 
        'ter': '티이알', 
        'test': '테스트', 
        'the': '더', 
        'thema': '테마', 
        'third': '썰드', 
        'threhat': '뜨뤳', 
        'three': '쓰리', 
        'tier': '티어', 
        'time': '타임', 
        'tippee': '티피', 
        'tiva': '티아이브이에이', 
        'to': '투', 
        'ttob': '티오비', 
        'tobin': '토빈', 
        'total': '토탈', 
        'trade': '트레이드', 
        'traded': '트레이디드', 
        'trading': '트레이딩', 
        'transfer': '트랜스퍼', 
        'treaty': '트뤼티', 
        'triffin': '트리핀', 
        'trout': '트로우트', 
        'trust': '트러스트', 
        'trusts': '트러스트스', 
        'umbrella': '엄브렐라', 
        'underwriter': '언더롸이터', 
        'underwriting': '언더롸이팅', 
        'unearned': '언이얼드', 
        'uneap': '유엔이피', 
        'unfair': '언페어', 
        'union': '유니온', 
        'united': '유나이티드', 
        'unlawful': '언러우풀', 
        'unsolicited': '언솔리시티드', 
        'unspecified': '언스페시파이드', 
        'use': '유즈', 
        'user': '유져', 
        'users': '유저스', 
        'value': '벨류', 
        'van': '브이에이엔', 
        'var': '브이에이알', 
        'variable': '배리어블', 
        'verification': '베리피케이션', 
        'voice': '보이스', 
        'volatilcity': '붤러틸러티', 
        'volcker': '볼컬', 
        'voting': '보팅', 
        'wall': '월', 
        'warning': '월닝', 
        'warrant': '워렌트', 
        'wash': '워시', 
        'weighted': '웨이티드', 
        'withdraw': '윗드로우', 
        'withdrawal': '윗드러울', 
        'without': '윗아웃', 
        'workout': '월크아웃', 
        'wrap': '뤱', 
        'wto': '떠블유티오', 
        'xbrl': '엑스비알엘', 
        'your': '유얼',
        "iii": "삼",
        "book": "북",
        "ii": "이",
        "capital": "캐피탈",
        "sut": "에스유티",
        "iv": "사",
        "tier": "티어",
        "additional": "에디셔널",
        "seacen": "",
        "escrow": "에스크로우",
        "vi": "육",
        "common": "커먼",
        "equity": "이퀴티",
        "tiva": "티바",
        "nafta": "나프타",
        "brexit": "브렉시트",
        "forward": "포워드",
        "guidance": "가이던스",
        "tables": "테이블스",
        "vii": "칠",
        "world": "월드",
        "bank": "뱅크",
        "viii": "팔",
        "ix": "구",
        "strips": "스트립스",
        "euro": "유로",
        "dollar": "달러",
        "market": "마켓",
        "euribor": "유리보",
        "dual": "듀얼",
        "currency": "큐런씨",
        "bond": "본드",
        "xi": "십일",
        "giro": "지로",
        "governance": "거버넌스",
        "moratorium": "모라토리엄",
        "total": "토탈",
        "return": "리턴",
        "swap": "스왑",
        "tapering": "테이퍼링",
        "taylor": "테일러",
        "rule": "룰",
        "tobin": "토빈",
        "tax": "택스",
        "xii": "십이",
        "monetary": "모네터리",
        "policy": "폴리시",
        "framework": "프레임워크",
        "triffin": "트리핀",
        "dilemma": "딜레마",
        "wire": "와이어",
        "xiii": "십삼",
        "repo": "레포",
        "beyond": "비욘드",
        "camel": "카멜",
        "roca": "로카",
        "debtrank": "뎁트랭크",
        "group": "그룹",
        "of": "오브",
        "two": "투",
        "seven": "세븐",
        "herstatt": "헐스탯",
        "kiko": "키코",
        "libor": "리보",
        "swift": "스위프트",
        "ted": "테드",
        "treasury": "트레저리",
        "bill": "빌",
        "van": "밴",
        "value": "밸류",
        "at": "엣",
        "risk": "리스크",
        "debt": "뎁트",
        "service": "써비스",
        "ratio": "레이시오",
        "to": "투",
        "asset": "에셋",
        "household": "하우스홀드",
        "income": "인컴",
        "and": "앤드",
        "social": "쏘셜",
        "transfer": "트랜스퍼",
        "in": "인",
        "kind": "카인드",
        "personal": "퍼스널",
        "disposable": "디스파서블",
        "gross": "그로스",
        "spread": "스프레드",
        "term": "텀",
        "basis": "베이시스",
        "point": "포인트",
        "virtual": "버츄얼",
        "digital": "디지털",
        "representation": "리프레젠테이션",
        "peer": "피어",
        "alt": "알트",
        "coin": "코인",
        "cryptocurrency": "크립토커런시",
        "initial": "이니셜",
        "offering": "오퍼링",
        "startup": "스타트업",
        "token": "토큰",
        "crowd": "크라우드",
        "funding": "펀딩",
        "legal": "리걸",
        "tender": "텐더",
        "public": "퍼빌릭",
        "coins": "코인즈",
        "etherium": "이더리움",
        "indirect": "인다이랙트",
        "financing": "파이낸싱",
        "direct": "다이랙트",
        "home": "홈",
        "country": "컨트리",
        "host": "호스트",
        "systemic": "시스태믹",
        "unwinding": "언와인딩",
        "resilience": "리사일런스",
        "spillover": "스필러버",
        "effects": "이팩츠",
        "large": "라지",
        "funds": "펀즈",
        "payment": "페이먼트",
        "system": "시스템",
        "fedwire": "페드와이어",
        "single": "싱글",
        "counterparty": "카운터파티",
        "connected": "커넥티드",
        "counterparties": "카운터파티즈",
        "settlement": "세틀먼트",
        "exchange": "익스체인지",
        "credit": "크레딧",
        "liquidity": "리퀴디티",
        "operational": "오퍼레이셔널",
        "loss": "로스",
        "sharing": "쉐어링",
        "defaulter": "디폴터",
        "pays": "페이즈",
        "survivors": "서바이버즈",
        "pay": "페이",
        "finality": "파이널리티",
        "iosco": "아이오스코",
        "universal": "유니버설",
        "banking": "뱅킹",
        "specialized": "스페셜라이즈드",
        "volcker": "볼커",
        "ring": "링",
        "fenced": "팬스드",
        "business": "비지니스",
        "conditions": "컨디션스",
        "cycle": "싸이클",
        "diffusion": "디퓨전",
        "index": "인덱스",
        "adjustment": "애드저스트먼트",
        "stabilization": "스태빌리제이션",
        "composite": "컴포짓",
        "eurostoxx": "유로스톡스",
        "decay": "디케이",
        "factor": "팩터",
        "nasdaq": "나스닥",
        "survey": "설베이",
        "consumer": "컨슈머",
        "economic": "이코노믹",
        "sentiment": "센티멘트",
        "organization": "올가니제이션",
        "for": "포",
        "cooperation": "코오퍼레이션",
        "development": "데벨롭먼트",
        "nordhaus": "노드하우스",
        "measure": "메쥬얼",
        "dow": "다우",
        "mutual": "뮤튜얼",
        "welfare": "웰페어",
        "know": "노우",
        "your": "유어",
        "customer": "커스터머",
        "verify": "버리파이",
        "anti": "안티",
        "money": "머니",
        "laundering": "라운더링",
        "straight": "스트레이트",
        "convertible": "컨버터블",
        "floating": "플로팅",
        "note": "노트",
        "consumption": "컨섬션",
        "fixed": "픽스드",
        "rate": "레이트",
        "free": "프리",
        "fundamentals": "펀다멘탈즈",
        "impossible": "임파서블",
        "trinity": "트리니티",
        "trilemma": "트릴레마",
        "okun": "오쿤",
        "misery": "미저리",
        "barrow": "바로우",
        "goldilocks": "골디락스",
        "economy": "이코노미",
        "the": "더",
        "three": "쓰리",
        "bears": "베어스",
        "open": "오픈",
        "operation": "오퍼레이션",
        "input": "인풋",
        "output": "아웃풋",
        "supply": "서플라이",
        "use": "유즈",
        "table": "테이블",
        "short": "숏",
        "selling": "셀링",
        "managed": "매니지드",
        "exchangeable": "익스체인져블",
        "bonds": "본즈",
        "with": "위드",
        "warrant": "워런트",
        "freely": "프릴리",
        "usable": "유저블",
        "criterion": "크라이테리언",
        "purchasing": "펄체이싱",
        "power": "파워",
        "parity": "패리티",
        "relief": "릴리프",
        "loan": "론",
        "moody": "무디",
        "fitch": "핏치",
        "sovereign": "소버린",
        "rating": "레이팅",
        "dbrain": "디브레인",
        "on": "온",
        "line": "라인",
        "real": "리얼",
        "time": "타임",
        "transaction": "트랜젝션",
        "processing": "프로세싱",
        "file": "파일",
        "protocol": "프로토콜",
        "stage": "스테이지",
        "domestic": "도메스틱",
        "claims": "클레임즈",
        "product": "프로덕트",
        "nominal": "노미널",
        "investment": "인베스먼트",
        "national": "내셔널",
        "account": "어카운트",
        "balance": "밸런스",
        "sheet": "시트",
        "net": "넷",
        "wealth": "웨스",
        "accounts": "어카운츠",
        "revenue": "래비뉴",
        "as": "에즈",
        "percentage": "퍼센티지",
        "security": "시큐리티",
        "contributions": "커트리뷰션",
        "fund": "펀드",
        "korea": "코리아",
        "china": "차이나",
        "foreign": "포린",
        "savings": "세이빙즈",
        "international": "인터네셔널",
        "settlements": "세틀먼츠",
        "financial": "파이낸셜",
        "derivatives": "디리버티브",
        "institute": "인스티튜트",
        "developing": "디벨로핑",
        "economies": "이코노미즈",
        "payments": "페이먼츠",
        "stock": "스톡",
        "flow": "플로우",
        "west": "웨스트",
        "texas": "텍사스",
        "intermediate": "인터미디에이트",
        "opec": "오팩",
        "petroleum": "페트롤리움",
        "export": "익스포트",
        "countries": "컨트리스",
        "quota": "쿼터",
        "reporting": "리포팅",
        "standards": "스탠다즈",
        "accounting": "어카운팅",
        "board": "보드",
        "primary": "프라이머리",
        "dealer": "딜러",
        "scale": "스케일",
        "regulatory": "레귤러터리",
        "sandbox": "샌드박스",
        "innovation": "이노베이션",
        "hub": "허브",
        "university": "유니버시티",
        "share": "쉐어",
        "aaa":"트리플에이",
        "bbb":"트리플비",
        "poc":"피오씨",
        "msci":"엠에스씨아이",
        'adr':'에이디알',
        'kddi':'케이디디아이',
        'hsbc':'에이치에스비씨',
        'tmr':'티엠알',
        'gnm':'지엔앰',
        'agro':'아그로',
        'orion':'오리온'
}

english_dictionary_number = {
        'b2b': '비투비', 
        'b2c': '비투씨',
        'p2p': '피투피',
        'tier1':'티어원',
        'tier2':'티어투',
        '2xl':'투엑스라지',
        '3xl':'쓰리엑스라지'
}
mail_dictionary = {
    "gmail": '쥐메일',
    "naver": '네이버',
    "daum":'다음',
    ".com":'닷컴',
    ".net":'닷넷'
}

symbol_dictionary = {
    '%': '퍼센트',
    '˚': '도',
    '&': '앤',
    "@": '엣',
    "#": '샵',
    "$": '달러',
    "℃": '도씨',
    "'s": '쯔'
}

num_to_kor = {
        '0': '영',
        '1': '일',
        '2': '이',
        '3': '삼',
        '4': '사',
        '5': '오',
        '6': '육',
        '7': '칠',
        '8': '팔',
        '9': '구',
}

num_to_kor_phone = {
        '0': '공',
        '1': '일',
        '2': '이',
        '3': '삼',
        '4': '사',
        '5': '오',
        '6': '육',
        '7': '칠',
        '8': '팔',
        '9': '구',
}

unit_to_kor1 = {
        'cm': '센치미터',
        'm': '미터',
        'km': '킬로미터',
        'g': '그램',
        'kg': '킬로그램',
        'μm': '마이크로미터',
        "nm": '나노미터',
        'μg': '마이크로그램',
        'ng': '나노그램',
        'v': '볼트',
        't': '톤',
        'db':'데시벨',
        'hz': '헤르츠',
        'ft': '피트',
        'in':'인치',
        'yd' : '야드',
        'l' : '리터'
}
unit_to_kor2 = {
        'mile' : '마일',
        'lb':'파운드',
        'ml':'밀리리터',
        'mg': '밀리그램',
        'mm': '밀리미터',
        'million' : '밀리언',
        'millions' : '밀리언즈'
}

# english_checker = "(km|kg|g|m|cm|μm|v)"
# english_checker2 = "(mg|mm)"

lower_to_kor = {
        'a': '에이',
        'b': '비',
        'c': '씨',
        'd': '디',
        'e': '이',
        'f': '에프',
        'g': '지',
        'h': '에이치',
        'i': '아이',
        'j': '제이',
        'k': '케이',
        'l': '엘',
        'm': '엠',
        'n': '엔',
        'o': '오',
        'p': '피',
        'q': '큐',
        'r': '알',
        's': '에스',
        't': '티',
        'u': '유',
        'v': '브이',
        'w': '더블유',
        'x': '엑스',
        'y': '와이',
        'z': '제트',
}

def compare_sentence_with_jamo(text1, text2):
    return h2j(text1) != h2j(text2)

def tokenize(text,as_id=False):
    # jamo package에 있는 hangul_to_jamo를 이용하여 한글 string을 초성/중성/종성으로 나눈다.
    text = normalize(text)
    tokens = list(hangul_to_jamo(text)) # '존경하는'  --> ['ᄌ', 'ᅩ', 'ᆫ', 'ᄀ', 'ᅧ', 'ᆼ', 'ᄒ', 'ᅡ', 'ᄂ', 'ᅳ', 'ᆫ', '~']

    if as_id:
        return [char_to_id[token] for token in tokens] + [char_to_id[EOS]], text
    else:
        return [token for token in tokens] + [EOS], text

def tokenizer_fn(iterator):
    return (token for x in iterator for token in tokenize(x, as_id=False))



#######
default_dictionary = {
    '10월' : '시월',
    '6월' : '유월',
    # '고점' : '고쩜',
    # '저점' : '저쩜',
    # '거점' : '거쩜',
    # '유가' : '유까',
    # '고가' : '고까',
    # '저가' : '저까',
    # '채권' : '채꿘',
    # '주가' : '주까',
    # '사건' : '사껀',
    # '수법' : '수뻡',
    # '평가' : '평까',
    '솔루션' : '쏠루션',
    # '물가' : '물까',
    # '상한가' : '상한까',
    # '하한가' : '하한까',
    # '공모가' : '공모까',
    '숲 속' : '숲속',
    '서비스' : '써비스',
    # '문자' : '문짜',
    '메시지' : '메씨지',
    '문득' : '문뜩',
    'S&P':'에스앤피',
    's&p':'에스앤피',
    'aaa-':'트리플에이마이너스',
    'AAA-':'트리플에이마이너스',
    'bbb-':'트리플비마이너스',
    'BBB-':'트리플비마이너스',
    '⓪':'영',
    '①':'일',
    '②':'이',
    '③':'삼',
    '④':'사',
    '⑤':'오',
    '⑥':'육',
    '⑦':'칠',
    '⑧':'팔',
    '⑨':'구',
    '⑩':'십',
    '⑪':'십일',
    '⑫':'십이'
    
}


def normalize(text):
    flag = False
    # # import pdb;pdb.set_trace()
    text = text.strip()
    text = re.sub("([A-Za-z]+)" + "([ㄱ-힣0-9]+)",
                lambda x: english_korean(x), text)
    text = re.sub("([ㄱ-힣0-9]+)" + "([A-Za-z]+)",
                lambda x: english_korean(x), text)
    text = normalize_with_dictionary(text,default_dictionary)
    text = normalize_englishword(text)  
    text = normalize_englishword_number(text)  
    text = normalize_englishword_number_check_unit(text)
    text = normalize_dash(text)
    text = normalize_slash(text)
    text = normalize_colon(text)
    text = normalize_wave(text)
    text = normalize_dot(text)
    if len(text) == 0:
        return ""
    if text[-1] == ".":
        flag =True
        text = text[:-1]
    text = normalize_number(text)
    # if model_name == 'female_Korean':
    #     text = text.replace(',','')
    text = normalize_with_dictionary(text, symbol_dictionary)
    text = normalize_with_dictionary(text, mail_dictionary)
    text = normalize_with_dictionary(text, chinese_dictionary)
    # text = hanja.translate(text, 'substitution') #######
    text = normalize_quote(text)
    text = text.replace("+","플러쓰")
    text = text.replace("±","플러쓰마이너스")
    text = re.sub('[.…]+', '.', text)
    text = re.sub('[\(\[\{<]+', ' ', text)
    text = re.sub('[\)\]\}\*\^>-]+', '', text)
    text = text.replace(":","")
    text = text.replace(";","")
    if len(text) == 0:
        return ""
    text = normalize_english(text)
    text = normalize_g2pk(text)
    text = normalize_korean(text)
    text = text.strip()
    if flag:
        text = text+'.'
    # if model_name == 'female_Korean':
    # text = end_remove(text)
    return text

def english_korean(str):
    str1, str2 = str.group(1), str.group(2)
    text = str1 + " " + str2
    return text

def end_remove(text):
    for n, _ in enumerate(text):
        if text[-(n+1)] == "." or text[-(n+1)] == "?" or text[-(n+1)] == "!" or text[-(n+1)] == "~":
            # print('debugging',text[-(n+1)],n)
            continue
        else:
            # print('debugging',text[-(n+1)])
            if (ord(text[-(n+1)]) - 44032) % 28:
                jamo_str = split_syllables(text[-(n+1)])
                
                # if jamo_str[-1] == 'ㅁ' or jamo_str[-1] == 'ㄴ' or jamo_str[-1] == 'ㅇ' or jamo_str[-2] == 'ㅏ':
                #     return text
                t = join_jamos(jamo_str[:-1])
                
                text = text[:-(n+1)]+t+text[-(n)]
                
                break
            else:
                break
    return text

def normalize_dot(text):
    def fn(m):
        word = m.group()
        # word_split = word.split('·')
        word = word.replace('·','')
        word = normalize_with_dictionary(word,num_to_kor_phone)
        return word
    text = re.sub(number_checker+'(·)'+number_checker,fn,text)
    return text

def normalize_wave(text):
    text = re.sub(number_checker+ wave_checker + number_checker + count_checker2,
                  lambda x: wav_to_korean(x), text)
    text = re.sub(number_checker + wave_checker + number_checker + custom_checker,
                  lambda x: wav_to_korean(x), text)
    text = re.sub(number_checker + wave_checker + number_checker + count_checker,
                  lambda x: wav_to_korean(x), text)
    text = re.sub("([A-Za-zㄱ-힣0-9]+)" + wave_checker + "([A-Za-zㄱ-힣0-9]+)",
                  lambda x: wav_to_korean(x, True), text)
    text = re.sub("[\~\→\∼]", "", text)
    return text

def wav_to_korean(num_str, is_count=False):
    # import pdb;pdb.set_trace()
    if is_count:
        str1, wav_str, str2 = num_str.group(1), num_str.group(2), num_str.group(3)
        result = str1 + "에서 " + str2
    else:
        num1_str, num2_str, count_str = num_str.group(1), num_str.group(3), num_str.group(4)
        if count_str == "개월":
            result = num1_str + "에서 " + num2_str + count_str
        else:
            result = num1_str + count_str + "에서 " + num2_str + count_str
    return result

def normalize_englishword(text):
    def fn(m):

        word = m.group()
        if word.lower() in english_dictionary_new:
            return english_dictionary_new.get(word.lower())

        else:
            return word
    
    text = re.sub("([A-Za-z]+)", fn, text)

    return text

def normalize_englishword_number(text):
    def fn(m):

        word = m.group()
        if word.isdigit(): #숫자만 있으면
            return word
        elif any(elem.isdigit() for elem in word) == False: #영어만 있으면
            return word
        ### dong ###
        if word.lower() in english_dictionary_number:
            return english_dictionary_number.get(word.lower()) 
        else:
            return word
        # elif word in unit_to_kor1:
        #     return unit_to_kor1.get(word)
        # elif word in unit_to_kor2:
        #     return unit_to_kor2.get(word)
        ### dong ###
    
    text = re.sub("([A-Za-z0-9]+)", fn, text)

    return text

def unit_read(unit_str):
    # unit_to_kor1 = {
    #     'cm': '센치미터',
    #     'm': '미터',
    #     'km': '킬로미터',
    #     'g': '그램',
    #     'kg': '킬로그램',
    #     'μm': '마이크로미터',
    #     "nm": '나노미터',
    #     'μg': '마이크로그램',
    #     'ng': '나노그램',
    #     'v': '볼트'
    # }
    # unit_to_kor2 = {
    #         'mg': '밀리그램',
    #         'mm': '밀리미터',
    #         'million' : '밀리언'
    # }
    if unit_str.lower() in unit_to_kor1.keys():
        return unit_to_kor1[unit_str.lower()]

    elif unit_str.lower() in unit_to_kor2.keys():
        return unit_to_kor2[unit_str.lower()]

    else :
        return normalize_smart_g2p(unit_str)

def normalize_englishword_number_check_unit(text):
    def fn(m):
        word = m.group()
        last_num_index = 0

        for a, char_a in enumerate(reversed(list(word))):
            if char_a.isalpha():
                continue
            else :
                last_num_index = a
                break

        # print(word)
        unit_cut = str(word[:len(word)-last_num_index] +  unit_read(word[len(word)-last_num_index:]))
        # print(unit_cut)
        return unit_cut

    text = re.sub(number_checker+english_checker, fn, text)
    
    return text


def normalize_phone_number(text):
    def fn(m):
        word = m.group()
        word = word.replace('-',' ')
        word = normalize_with_dictionary(word,num_to_kor_phone)
        return word
    text = re.sub("\s*(?:\+?(\d{1,3}))?[-(]*(\d{3,4})[-)]*(\d{3,4})[-]*(\d{0,4})(?: *x(\d+))?\s*", fn, text)
    return text

def normalize_date(text):
    def fn(m):
        word =m.group()
        word_split = word.split('-')
        return f"{word_split[0]}년 {word_split[1]}월 {word_split[2]}일"
    text = re.sub(number_checker+'(-)'+number_checker+'(-)'+number_checker,fn,text)
    return text

def normalize_korean(text):
    def fn(m):
       return ""
    # text = re.sub('((\d{4})|\d{2})?(-|/|.)?(?P<month>[1-9]|0[1-9]|1[0-2])(-|/|.|월 )(?P<date>([1-9]|0[1-9]|[1-2][0-9]|3[01]))일?$',fn,text)
    text = re.sub(korean_checker,fn,text)
    return text

def normalize_date_with_slash(text):
    def fn(m):
        word = m.group()
        word = word.replace(',','')
        word_split = word.split('/')
        if float(word_split[0]) >0 and float(word_split[0]) <13 and float(word_split[1]) >0 and float(word_split[1])<32:
            return f"{word_split[0]}월 {word_split[1]}일"    
        else:
            return word.replace('/', ' ')
    # text = re.sub('((\d{4})|\d{2})?(-|/|.)?(?P<month>[1-9]|0[1-9]|1[0-2])(-|/|.|월 )(?P<date>([1-9]|0[1-9]|[1-2][0-9]|3[01]))일?$',fn,text)
    text = re.sub('([+-]?\d[\d,]*)[\.]?\d*(/)([+-]?\d[\d,]*)[\.]?\d*',fn,text)
    return text

def normalize_date_with_colon(text):
    def fn(m):
        word = m.group()
        word = word.replace(',','')
        word_split = word.split(':')
        try:
            if len(word_split[0]) == 2 or len(word_split[1]) == 2:
                if int(word_split[0]) >=0 and int(word_split[0]) <25 and int(word_split[1]) >=0 and int(word_split[1])<60:
                    if int(word_split[1]) == 0:
                        return f"{int(word_split[0])}시"        
                    else:
                        return f"{int(word_split[0])}시 {int(word_split[1])}분"
                else:
                    return f"{word_split[0]}대 {word_split[1]}"
            else:
                return f"{word_split[0]}대 {word_split[1]}"
        except:
            return f"{word_split[0]}대 {word_split[1]}"
    # text = re.sub('((\d{4})|\d{2})?(-|/|.)?(?P<month>[1-9]|0[1-9]|1[0-2])(-|/|.|월 )(?P<date>([1-9]|0[1-9]|[1-2][0-9]|3[01]))일?$',fn,text)
    text = re.sub('([+-]?\d[\d,]*)[\.]?\d*(:)([+-]?\d[\d,]*)[\.]?\d*',fn,text)
    return text


def normalize_code_num(text):
    
    def fn(m):
        word = m.group()
        word = word.replace('-','다시 ')
        return word
    return re.sub(number_checker+code_checker+number_checker,fn,text)

def normalize_code_num_2(text):
    def fn(m):
        word = m.group()
        word = word.replace('-',' ')
        word = normalize_with_dictionary(word,num_to_kor_phone)
        return word

    return re.sub(english_checker+code_checker+number_checker,fn,text)

def normalize_dash(text):
    
    text = normalize_phone_number(text) # 폰 번호 거르고
    text = normalize_date(text) # 날짜 거르고
    text = normalize_code_num(text) # 앞뒤 숫자면 다시로 읽고 12-1
    text = normalize_code_num_2(text) # covid-19 -> covid 19 #여기서 안없애주면 마이너스 십구라 읽음
    # text = normalize_number(text) # 숫자로 바꾸고
    # text = text.replace('-',' ') # 나머지는 다 없애버리자
    return text

def normalize_slash(text):
    text = normalize_date_with_slash(text)
    text = text.replace('/',' ')
    return text


def normalize_colon(text):
    text = normalize_date_with_colon(text)
    return text

def normalize_smart_g2p(text):
    texts = ""
    token = ""
    for n, i in enumerate(text):
        if n == len(text)-1:
            token += i
            texts += trans(token)
            token = ""
        else:
            if i == " ":
                texts += trans(token)+" "
                token = ""
            else:
                token += i
    return texts

def normalize_g2pk(text):
    texts = ""
    token = ""
    for n, i in enumerate(text):
        if n == len(text)-1:
            token += i
            texts += g2p(token)
            token = ""
        else:
            if i == " ":
                texts += g2p(token)+" "
                token = ""
            else:
                token += i
    return texts

def normalize_with_dictionary(text, dic):
    if any(key in text for key in dic.keys()):
        pattern = re.compile('|'.join(re.escape(key) for key in dic.keys()))
        return pattern.sub(lambda x: dic[x.group()], text)
    else:
        return text

def normalize_english(text):
    def fn(m):
        word = m.group()
        if word.isupper(): #다 대문자면
            if len(word) >=4: #4자 이상이면 g2pk
                word = normalize_smart_g2p(word.lower())
            else: #3자 이하면
                word = normalize_with_dictionary(word.lower(),lower_to_kor)
        else:# 대소문자가 섞여있으면
            word = normalize_smart_g2p(word.lower())    
        return word
    
    text = re.sub("([A-Za-z]+)", fn, text)

    return text

def normalize_lower(text):
    text = text.group(0)
    text = text.lower()
    if all([char.islower() for char in text]):
        return "".join(lower_to_kor[char] for char in text)
    else:
        return text

def normalize_quote(text):
    def fn(found_text):
        from nltk import sent_tokenize # NLTK doesn't along with multiprocessing

        found_text = found_text.group()
        unquoted_text = found_text[1:-1]

        sentences = sent_tokenize(unquoted_text)
        return " ".join(["{}".format(sent) for sent in sentences])

    return re.sub(quote_checker, fn, text)

number_checker = "([+-]?\d[\d,]*)[\.]?\d*"
count_checker = "(곳|방|시|명|가지|살|마리|포기|송이|수|톨|통|벌|척|채|개|다발|그루|자루|줄|켤레|문장|그릇|잔|마디|상자|사람|곡|병|판|배)" #개를 뺌 #########
custom_checker = "(개월)"
count_checker2 = "(시간|시즌|방울)"
english_unit_checker = "(km|kg|g|m|cm|μm|v)"
english_unit_checker2 = "(mg|mm|million)"
code_checker = "(-)"
english_checker ="([A-Za-z]+)"
korean_checker ="([ㄱ-ㅎㅏ-ㅣ]+)"
money_checker = "(\$|\₩)"
wave_checker = "(\~|\→|\∼)"

def normalize_number(text):
    text = re.sub(number_checker+ custom_checker,
            lambda x: number_to_korean(x, True), text)
    text = re.sub(number_checker + count_checker,
            lambda x: number_to_korean(x, True), text)
    # text = re.sub(number_checker + english_unit_checker2,
    #     lambda x: number_to_korean(x, False, False, False, True), text)
    # text = re.sub(number_checker + english_unit_checker,
    #     lambda x: number_to_korean(x, False, False, True), text)
    text = re.sub(money_checker + number_checker,
        lambda x: number_to_korean(x, False, True), text)
    text = re.sub(number_checker,
            lambda x: number_to_korean(x, False), text)
    return text

num_to_kor1 = [""] + list("일이삼사오육칠팔구")
num_to_kor2 = [""] + list("만억조경해")
num_to_kor3 = [""] + list("십백천")

#count_to_kor1 = [""] + ["하나","둘","셋","넷","다섯","여섯","일곱","여덟","아홉"]
count_to_kor1 = [""] + ["한","두","세","네","다섯","여섯","일곱","여덟","아홉"]

count_tenth_dict = {
        "십": "열",
        "두십": "스물",
        "세십": "서른",
        "네십": "마흔",
        "다섯십": "쉰",
        "여섯십": "예순",
        "일곱십": "일흔",
        "여덟십": "여든",
        "아홉십": "아흔",
}

count_tenth_dict_no_count = {
        "일십": "십",
        "일백": "백",
        "일천": "천"
}



def number_to_korean(num_str, is_count=False, is_money=False, is_english1=False, is_english2=False):
    if is_count:
        num_str, unit_str = num_str.group(1), num_str.group(2)
        num_str = num_str.replace(',', '')
        if int(num_str) > 100:
            is_count = False
        if unit_str == "개월":
            is_count = False
        if unit_str == "시" and int(num_str) >= 13:
            is_count = False
    else:
        if is_money:
            unit_str, num_str = num_str.group(1), num_str.group(2)
        else:
            if is_english1:
                num_str, unit_str= num_str.group(1), unit_to_kor1.get(num_str.group(2))
            else:
                if is_english2:
                    num_str, unit_str= num_str.group(1), unit_to_kor2.get(num_str.group(2))
                else:
                    num_str, unit_str = num_str.group(), ""
        num_str = num_str.replace(',', '')
    # num = ast.literal_eval(num_str)

    # if num == 0:
    #     return "영"

    check_float = num_str.split('.')
    if len(check_float) == 2:
        digit_str, float_str = check_float
    elif len(check_float) >= 3:
        raise Exception(" [!] Wrong number format")
    else:
        digit_str, float_str = check_float[0], None

    if is_count and float_str is not None:
        raise Exception(" [!] `is_count` and float number does not fit each other")

    digit = int(digit_str)
    
    if digit_str.startswith("-") or digit_str.startswith("+"):
        digit, digit_str = abs(digit), str(abs(digit))

    kor = ""
    if digit_str == '0':
        kor+="영"
    elif digit_str.startswith('0'):
        digit_str=digit_str[1:]
        
    size = len(str(digit))
    tmp = []

    for i, v in enumerate(digit_str, start=1):
        v = int(v)

        if v != 0:
            if is_count:
                tmp += count_to_kor1[v]
            else:
                tmp += num_to_kor1[v]

            tmp += num_to_kor3[(size - i) % 4]

        if (size - i) % 4 == 0 and len(tmp) != 0:
            kor += "".join(tmp)
            tmp = []
            kor += num_to_kor2[int((size - i) / 4)]

    if is_count:
        if kor.startswith("한") and len(kor) > 1:
            kor = kor[1:]

        if any(word in kor for word in count_tenth_dict):#들여쓰기
            kor = re.sub(
                    '|'.join(count_tenth_dict.keys()),
                    lambda x: count_tenth_dict[x.group()], kor)

    if not is_count and kor.startswith("일") and len(kor) > 1:
        kor = kor[1:]
    if not is_count:
        if any(word in kor for word in count_tenth_dict_no_count):
            kor = re.sub(
                    '|'.join(count_tenth_dict_no_count.keys()),
                    lambda x: count_tenth_dict_no_count[x.group()], kor)


    if float_str is not None:
        kor += "쩜"
        kor += re.sub('\d', lambda x: num_to_kor[x.group()], float_str)

    if num_str.startswith("+"):
        kor = " 플러스 " + kor
    elif num_str.startswith("-"):
        kor = " 마이너스 " + kor

    return kor + unit_str

if __name__ == "__main__":
    import time
    
    def test_normalize(text):
        start_time = time.time()
        print(normalize(text,{}))
        end_time = time.time()
        
        print(end_time - start_time)
        print("="*30)

    # test_normalize("우량주를 모아놓은 S&P 500지수는 올해 20% 가까이 떨어지면서 1970년 이후 가장 큰 하락폭을 기록하는가 하면, 미 국채 가격도 10%나 폭락했습니다.")
    test_normalize("3개")
    test_normalize("세계")
    # test_normalize("안녕하세요~")
    # test_normalize("서울~부산")