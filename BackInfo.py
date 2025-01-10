from bs4 import BeautifulSoup
import requests
import errors as error
import json
import html
headers = {'accept': 'application/json, text/javascript, */*; q=0.01','accept-language': 'ru,en;q=0.9','x-requested-with': 'XMLHttpRequest'}

class AnimeResult:
    def __init__(self,q:str,lxml:str):
        self.upload = {}
        self.page = 1
        self.pages_end = False
        self.q = q
        self.lxml = lxml
        params = {'q': q}
        response = requests.get('https://animego.me/search/anime',headers=headers,params=params)
        self.soup = BeautifulSoup(response.text,lxml)
        try:
            self.all_page:int = int(self.soup.find('span',class_="search-county align-top mb-2").text)
        except AttributeError:
            raise error.NotFoundError("по вашему запросу ничего не найдено")
        self.upload[self.page] = self.first_page()
    
    def first_page(self):
        self.pages_end = False
        self.page = 1
        if self.upload.get(self.page):
            return self.upload.get(self.page)
        back_info = {}
        all_anime = self.soup.find_all('div', class_="animes-grid-item col-6 col-sm-6 col-md-4 col-lg-3 col-xl-2 col-ul-2")
        back_info['page_num'] = self.page
        all_animes = {}
        for anime in all_anime:
            anime_link = anime.find("a", attrs={"data-ajax-url": True})["href"]
            image_poster = anime.find("div", class_="anime-grid-lazy")["data-original"]
            anime_title = anime.find("a", title=True)["title"]
            anime_id = ''.join([char for char in anime_link if char.isdigit()])
            all_animes[anime_id] = {'anime_title':anime_title,'anime_link':anime_link,'image_poster':image_poster}
        back_info['all_anime'] = all_animes
        return back_info
    
    
    def next_page(self):
        if self.pages_end: return 'pages-end'
        self.page += 1
        if self.upload.get(self.page):
            return self.upload.get(self.page)
        back_info = {}
        params = {'q': self.q,'type': 'list','page': self.page}
        response = requests.get('https://animego.me/search/anime',headers=headers,params=params)
        js:dict = response.json()
        if js.get('status') != 'success': return js.get('status')
        if js.get('endPage') == True: self.pages_end = True
        soup = BeautifulSoup(js.get('content'),self.lxml)
        all_anime = soup.find_all('div', class_="animes-grid-item col-6 col-sm-6 col-md-4 col-lg-3 col-xl-2 col-ul-2")
        back_info['page_num'] = self.page
        all_animes = {}
        for anime in all_anime:
            anime_link = anime.find("a", attrs={"data-ajax-url": True})["href"]
            image_poster = anime.find("div", class_="anime-grid-lazy")["data-original"]
            anime_title = anime.find("a", title=True)["title"]
            anime_id = ''.join([char for char in anime_link if char.isdigit()])
            all_animes[anime_id] = {'anime_title':anime_title,'anime_link':anime_link,'image_poster':image_poster}
        back_info['all_anime'] = all_animes
        self.upload[self.page] = back_info
        return back_info
        
    def back_page(self):
        self.pages_end = False
        if self.page == 1: return 'это первая страница'
        self.page -= 1
        if self.upload.get(self.page):
            return self.upload.get(self.page)
        back_info = {}
        params = {'q': self.q,'type': 'list','page': self.page}
        response = requests.get('https://animego.me/search/anime',headers=headers,params=params)
        js:dict = response.json()
        if js.get('status') != 'success': return js.get('status')
        soup = BeautifulSoup(js.get('content'),self.lxml)
        all_anime = soup.find_all('div', class_="animes-grid-item col-6 col-sm-6 col-md-4 col-lg-3 col-xl-2 col-ul-2")
        back_info['page_num'] = self.page
        all_animes = {}
        for anime in all_anime:
            anime_link = anime.find("a", attrs={"data-ajax-url": True})["href"]
            image_poster = anime.find("div", class_="anime-grid-lazy")["data-original"]
            anime_title = anime.find("a", title=True)["title"]
            anime_id = ''.join([char for char in anime_link if char.isdigit()])
            all_animes[anime_id] = {'anime_title':anime_title,'anime_link':anime_link,'image_poster':image_poster}
        back_info['all_anime'] = all_animes
        self.upload[self.page] = back_info
        return back_info
        
class AnimeFindResult:
    def res(link:str, use_lxml:str):
        back_dict = {}
        r = requests.get(link,headers=headers)
        r.raise_for_status()
        dds = 0
        soup = BeautifulSoup(r.text,use_lxml)
        title = soup.find('div',class_="anime-title").text
        back_dict['название'] = title
        row = soup.find('dl', class_="row")
        dt = row.find_all('dt')
        dd = row.find_all('dd')
        for _ in range(len(dt)):
            tmp_dd = dd[_ + dds].text.strip().replace('\n','')
            tmp_dd = ' '.join(tmp_dd.split())
            tmp_dt = dt[_].text.strip()
            if not tmp_dd: 
                dds += 1
                tmp_dd = dd[_ + dds].text.strip().replace('\n','')
                tmp_dd = ' '.join(tmp_dd.split())
            back_dict[tmp_dt] = tmp_dd
        back_dict['ссылка'] = r.url
        try:
            back_dict['ссылка на постер'] = soup.find('img')['srcset'].replace(' 2x','')
        except KeyError:
            back_dict['ссылка на постер'] = soup.find('img')['src']
        
        return back_dict

class AnimeMpdFile:
    def get(id:int|str,episode:int|str,translation_id:int|str,lxml:str) -> str:
        """
            Получает параметры видео.

            - id: Уникальный идентификатор аниме, который находится в конце ссылки. 
                    
                    Пример: 2745 для аниме "Не моя вина, что я не популярна" 
                    
                    (ссылка: https://animego.me/anime/ne-moya-vina-chto-ya-ne-populyarna-2745).
            
            - episode: 
                    
                    Номер серии аниме. 
                    
                    Примеры: 1, 2, 3 и т.д.
            
            - translation_id: 
                    
                    Идентификатор перевода. 
                    
                    Примеры:
                        - 2 для Anilibria
                        - 3 для Kodik и т.д.
        """
        headers = {'x-requested-with': 'XMLHttpRequest',}
        params = {"_allow":True}
        response = requests.get(f'https://animego.me/anime/{str(id)}/player', headers=headers,params=params)
        response.raise_for_status()
        soup = BeautifulSoup(response.json()["content"],lxml)
        url = soup.find('span', class_="video-player-toggle-item text-truncate mb-1 br-3")['data-player'].split('?')[0]
        return AnimeMpdFile.get_aniboom(episode=episode,translation=translation_id,url=url)
        
    def get_aniboom(episode,translation,url):
        headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ru,en;q=0.9',
        'priority': 'u=0, i',
        'referer': 'https://animego.me/',
        }
        params = {'episode': str(episode),'translation': str(translation)}
        response = requests.get(f'https:{url}', params=params, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text,'lxml')
        video = soup.find('div', id="video")['data-parameters']
        decoded_json = html.unescape(video)
        data = json.loads(decoded_json)
        dash_data = json.loads(data['dash'])
        return dash_data['src']

class AnimeTranslationID:
    def get_all_TranslationID(id:int|str,lxml:str):
        back_inf = {}
        headers = {'x-requested-with': 'XMLHttpRequest',}
        params = {"_allow":True}
        response = requests.get(f'https://animego.me/anime/{str(id)}/player', headers=headers,params=params)
        response.raise_for_status()
        soup = BeautifulSoup(response.json()["content"],lxml)
        alls = soup.find_all('span', class_="video-player-toggle-item d-inline-block text-truncate mb-1 br-3 cursor-pointer")
        for i in alls:
            back_inf[i.text.strip()] = i['data-dubbing']
        return back_inf
        