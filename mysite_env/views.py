import datetime
from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum
from django.core.cache import cache
from django.utils import timezone
from read_statistics.utils import get_seven_days_read_date, get_today_hot_data, get_yesterday_hot_data
from blog.models import Blog

def get_7_day_hot_blogs(days):
    today = timezone.now().date()
    date = today - datetime.timedelta(days=days)
    blogs = Blog.objects.filter(read_details__date__lt=today, read_details__date__gte=date) \
                        .values('id', 'title') \
                        .annotate(read_num_sum=Sum('read_details__read_num')) \
                        .order_by('-read_num_sum')
    return blogs[:7]

def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_days_read_date(blog_content_type)

    #获取7天热门博客缓存数据
    hot_blogs_for_7_days = cache.get('hot_blogs_for_7_days')
    if hot_blogs_for_7_days is None:
        hot_blogs_for_7_days = get_7_day_hot_blogs(7)
        cache.set('hot_blogs_for_7_days', hot_blogs_for_7_days, 3600)
        print('calc')
    else:
        print('use cache')
    context = {}
    context['dates'] = dates
    context['read_nums'] = read_nums
    context['today_hot_data'] = get_today_hot_data(blog_content_type)
    context['yesterday_hot_data'] = get_yesterday_hot_data(blog_content_type)
    context['hot_blogs_for_7_days'] = get_7_day_hot_blogs(7)
    context['hot_blogs_for_30_days'] = get_7_day_hot_blogs(30)
    return render(request, "home.html", context)
