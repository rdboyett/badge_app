from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    (r'^logout/$', 'django.contrib.auth.views.logout',{'next_page': '/logoutSuccess'}),
)

urlpatterns = patterns('badge_app.views',
    (r'^checkUser/$', 'checkUser'),
    (r'^checkSessionLogin/$', 'checkSessionLogin'),
    #(r'^updateBadges/$', 'updateBadges'),
    (r'^badgeManager/$', 'badgeManager'),
    (r'^createBadge/$', 'createBadge'),
    (r'^editBadge/$', 'editBadge'),
    (r'^badgeInfo/$', 'badgeInfo'),
    (r'^awardBadge/$', 'awardBadge'),
    (r'^viewUserBadges/$', 'viewUserBadges'),
    (r'^getBadgesExtension/$', 'getBadgesExtension'),
    (r'^getMarqueeExtension/$', 'getMarqueeExtension'),
    (r'^getQuoteExtension/$', 'getQuoteExtension'),
    
)
