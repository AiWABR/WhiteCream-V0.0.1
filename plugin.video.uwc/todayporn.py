import urllib, urllib2, re, cookielib, os.path, sys, socket
import xbmc, xbmcplugin, xbmcgui, xbmcaddon

import utils

# 90 TPMain
# 91 TPList
# 92 TPPlayvid
# 93 TPCat
# 94 TPSearch
# 95 TPPornstars

def TPMain():
    utils.addDir('[COLOR yellow]Categories[/COLOR]','http://www.todayporn.com/channels/',93,'','')
    utils.addDir('[COLOR yellow]Pornstars[/COLOR]','http://www.todayporn.com/pornstars/page1.html',95,'','')
    utils.addDir('[COLOR yellow]Top Rated[/COLOR]','http://www.todayporn.com/top-rated/a/page1.html',91,'','')
    utils.addDir('[COLOR yellow]Most Viewed[/COLOR]','http://www.todayporn.com/most-viewed/a/page1.html',91,'','')
    utils.addDir('[COLOR yellow]Search[/COLOR]','http://www.todayporn.com/search/page1.html?q=',94,'','')
    TPList('http://www.todayporn.com/page1.html',1)
    xbmcplugin.endOfDirectory(utils.addon_handle)


def TPList(url, page):
    listhtml = utils.getHtml(url, '')
    match = re.compile('prefix="([^"]+)[^<]+[^"]+"([^"]+)">([^<]+)<[^"]+[^>]+>([^\s]+)\s', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for thumb, videourl, name, duration in match:
        name = utils.cleantext(name)
        videourl = "http://www.todayporn.com" + videourl
        thumb = thumb + "1.jpg"
        name = name + " [COLOR blue]" + duration + "[/COLOR]"
        utils.addDownLink(name, videourl, 92, thumb, '')
    if re.search('Next &raquo;</a>', listhtml, re.DOTALL | re.IGNORECASE):
        npage = page + 1        
        url = url.replace('page'+str(page),'page'+str(npage))
        utils.addDir('Next Page ('+str(npage)+')', url, 91, '', npage)
    xbmcplugin.endOfDirectory(utils.addon_handle)


def TPPlayvid(url, name, download=None):
    videopage = utils.getHtml(url, '')
    match = re.compile("url: '([^']+flv)'", re.DOTALL | re.IGNORECASE).findall(videopage)
    if match:
        videourl = match[0]
        if download == 1:
            utils.downloadVideo(videourl, name)
        else:
            iconimage = xbmc.getInfoImage("ListItem.Thumb")
            listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
            listitem.setInfo('video', {'Title': name, 'Genre': 'Porn'})
            xbmc.Player().play(videourl, listitem)


def TPCat(url):
    caturl = utils.getHtml(url, '')
    match = re.compile('<img src="([^"]+)"[^<]+<[^"]+"([^"]+)">([^<]+)<', re.DOTALL | re.IGNORECASE).findall(caturl)
    for thumb, caturl, cat in match:
        caturl = "http://www.todayporn.com" + caturl + "page1.html"
        utils.addDir(cat, caturl, 91, thumb, 1)
    xbmcplugin.endOfDirectory(utils.addon_handle)


def TPPornstars(url, page):
    pshtml = utils.getHtml(url, '')
    pornstars = re.compile("""img" src='([^']+)'[^<]+<[^"]+"([^"]+)"[^>]+>([^<]+)<.*?total[^>]+>([^<]+)<""", re.DOTALL | re.IGNORECASE).findall(pshtml)
    for img, psurl, title, videos in pornstars:
        psurl = "http://www.todayporn.com" + psurl + "page1.html"
        title = title + " [COLOR blue]" + videos + "[/COLOR]" 
        utils.addDir(title, psurl, 91, img, 1)
    if re.search('Next &raquo;</a>', pshtml, re.DOTALL | re.IGNORECASE):
        npage = page + 1
        url = url.replace('page'+str(page),'page'+str(npage))
        utils.addDir('Next Page ('+str(npage)+')', url, 95, '', npage)        
    xbmcplugin.endOfDirectory(utils.addon_handle)
    

def TPSearch(url):
    searchUrl = url
    vq = utils._get_keyboard(heading="Searching for...")
    if (not vq): return False, 0
    title = urllib.quote_plus(vq)
    title = title.replace(' ','+')
    searchUrl = searchUrl + title + "&s=new"
    print "Searching URL: " + searchUrl
    TPList(searchUrl, 1)