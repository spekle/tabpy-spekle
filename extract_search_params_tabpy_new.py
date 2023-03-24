from tabpy.tabpy_tools.client import Client
from itertools import chain, combinations
from fuzzywuzzy import fuzz, process


def extract_search_params(search_sentence):
    script_dict = {
        'trx': ['claims', 'rx', 'trx', 'total'],
        'nrx': ['new', 'nrx', 'new claims'],
        'nbrx': ['nbrx', 'nbrx', 'new to brand'],
    }

    metric_dict = {'market share': ['share', 'market share'],
                   'volume': ['volume', 'demand', 'scripts', 'utilization', 'business', 'claims'],
                   'contribution': ['contribution'],
                   'claim volume': ['claim volume'],
                   'approval rate': ['approval rate', 'rejection rate'],
                   'nrx abandonment rate': ['abandonment rate'],
                   'nrx fulfilment rate': ['fulfilment rate'],
                   'oop cost': ['patient oop', 'oop', 'oop cost', 'patient out of pocket cost'],
                   'payer mix': ['payer mix', 'channel contribution', 'channel mix'],
                   'indication mix': ['indication mix', 'indication contribution'],
                   'patients': ['total patient', 'count patients', 'many patients', 'patient count'],
                   'nbrx patients': ['nbrx patient', 'nbrx patients', 'new brand patients'],
                   'bio-naive': ['bio naive', 'bio-naive', 'ntb market', 'ntb naive'],
                   'patient switch': ['switch', 'switching', 'patient switch', 'patients switching', 'patient switching'],
                   'rejection reasons': ['rejection reasons', 'rejections'],
                   'lis contribution': ['lis patient contribution', 'lis contribution', '% lis contribution'],
                   'willingness to pay': ['willingness pay', 'willingness pay curve', 'ability pay', 'ability pay curve', 'abandonment increase with patient oop increase']
                   }

    brand_dict = {'enbrel': ['enbrel'],
                  'humira': ['humira'],
                  'otezla': ['otezla'],
                  'siliq': ['siliq'],
                  'simponi': ['simponi'],
                  'rinvoq': ['rinvoq'],
                  'skyrizi': ['skyrizi'],
                  'olumiant': ['olumiant'],
                  'cosentyx': ['cosentyx'],
                  'xeljanz': ['xeljanz'],
                  'ilumya': ['ilumya'],
                  'kevzara': ['kevzara'],
                  'kineret': ['kineret'],
                  'stelara': ['stelara'],
                  'taltz': ['taltz'],
                  'actemra': ['actemra'],
                  'cimzia': ['cimzia'],
                  'orencia': ['orencia'],
                  'tremfya': ['tremfya']
                  }

    timeperiod_dict = {'ytd': ['ytd', 'this year'],
                       '2021': ['2021'],
                       '2022': ['2022'],
                       '2020': ['2020'],
                       'r24m': ['last 24 months', 'r24', 'r24m', 'last 2 years', 'last two years'],
                       'r12m': ['last 12 months', 'r12', 'r12m'],
                       'r6m': ['last 6 months', 'r6', 'r6m'],
                       'r3m': ['last 3 months', 'r3', 'r3m'],
                       'r13w': ['last 13 weeks', 'r13w']
                       }

    timegap_dict = {'month': ['monthly', 'by month'],
                    'week': ['weekly', 'by week'],
                    'year': ['yearly', 'by year'],
                    'quarter': ['quarterly', 'by quarter']
                    }

    channel_dict = {'commercial': ['commercial', 'third party', 'commercial channel', 'comm'],
                    'medicare': ['medicare', 'medicare channel'],
                    # 'medicare part d': ['medicare part d', 'part d'],
                    # 'pdp': ['pdp'],
                    # 'mapd': ['medicare advantage part d', 'mapd'],
                    # 'medicare advantage': ['medicare advantage', 'medicare advantage channel'],
                    # 'medicare ffs': ['medicare ffs', 'ffs medicare', 'mac b', 'mac'],
                    'medicaid': ['medicaid'],
                    'state medicaid': ['state medicaid', 'ffs medicaid', 'medicaid ffs'],
                    'managed medicaid': ['managed medicaid'],
                    # 'all channels': ['all channels', 'all method of payment', 'all payment types']
                    }
    indication_dict = {'pso': ['pso', 'psoriasis'],
                       'psa': ['psa', 'psoriatic arthritis'],
                       'ra': ['ra', 'rheumatoid arthritis'],
                       'uc': ['uc', 'ulcerative colitis'],
                       'cd': ['cd', 'chrons disease', 'chrons'],
                       'as': ['as', 'ankyliting spondylitis']
                       }
    controller_dict = {'united': ['uhg', 'uhc', 'united health group', 'united health', 'united'],
                       'optum': ['optum', 'optumrx'],
                       'express': ['express scripts inc', 'esi', 'express scripts'],
                       'anthem': ['anthem', 'anthem inc'],
                       'bcbsnc': ['bcbs nc', 'blue cross blue shield of north carolina', 'bcbs north carolina'],
                       'cvs': ['cvs', 'caremark', 'cvs caremark']
                       }

    visualization_dict = {'histogram': ['histogram', 'buckets', 'distribution'],
                          'line chart': ['trend', 'trend line'],
                          'pie chart': ['pie'],
                          'table': ['table', 'tabular', 'data dump']
                          }

    def match_dict(search_word, dictionary):
        direct_match = [k for k, v in dictionary.items() if search_word in v]
        if direct_match:
            return direct_match[0]

        best_match = process.extractOne(
            search_word, dictionary.keys(), scorer=fuzz.token_sort_ratio)
        if best_match[1] > 70:
            return best_match[0]
        else:
            return ''

    def get_combinations(words):
        return list(chain.from_iterable(combinations(words, r) for r in range(1, min(4, len(words)) + 1)))

    search_words = search_sentence.lower().split()
    search_params = {
        'script': 'TRx',
        'metric': 'Volume',
        'brand': '',
        'timeperiod': '',
        'channel': '',
        'indication': '',
        'controller': '',
        'visualization': '',
        'timegap': '',
        'cut_by': ''
    }

    search_combinations = get_combinations(search_words)
    for search_combo in search_combinations:
        search_phrase = ' '.join(search_combo)
        search_params['script'] = match_dict(
            search_phrase, script_dict) or search_params['script']
        search_params['metric'] = match_dict(
            search_phrase, metric_dict) or search_params['metric']
        search_params['brand'] = match_dict(
            search_phrase, brand_dict) or search_params['brand']
        search_params['timeperiod'] = match_dict(
            search_phrase, timeperiod_dict) or search_params['timeperiod']
        search_params['channel'] = match_dict(
            search_phrase, channel_dict) or search_params['channel']
        search_params['indication'] = match_dict(
            search_phrase, indication_dict) or search_params['indication']
        search_params['controller'] = match_dict(
            search_phrase, controller_dict) or search_params['controller']
        search_params['visualization'] = match_dict(
            search_phrase, visualization_dict) or search_params['visualization']
        search_params['timegap'] = match_dict(
            search_phrase, timegap_dict) or search_params['timegap']

        if 'by' in search_combo:
            cut_by_candidate = ' '.join(
                search_combo[search_combo.index('by') + 1:])
            if cut_by_candidate in ['controller', 'channel', 'indication', 'brand']:
                search_params['cut_by'] = cut_by_candidate

    return search_params


client = Client('http://localhost:9004/')

# print(extract_search_params("otezla market share"))
client.deploy('get_entities', extract_search_params,
              'extracts search params', override=True)


# host it on a server
# publish it and see
