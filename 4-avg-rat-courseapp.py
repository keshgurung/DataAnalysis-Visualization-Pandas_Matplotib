import justpy as jp
import pandas
from datetime import datetime
from pytz import utc


data=pandas.read_csv('reviews.csv', parse_dates=['Timestamp']) 
data['Month'] = data['Timestamp'].dt.strftime('%Y-%m')
month_avg_course = data.groupby(['Month','Course Name']).mean().unstack() 
# we will have multi index month n course name



chart_def = """
{
    chart: {
        type: 'areaspline'
    },
    title: {
        text: 'Average fruit consumption during one week'
    },
    legend: {
        layout: 'vertical',
        align: 'left',
        verticalAlign: 'top',
        x: 150,
        y: 100,
        floating: true,
        borderWidth: 1
    },
    xAxis: {
        categories: [
            'Monday',
            'Tuesday',
            'Wednesday',
            'Thursday',
            'Friday',
            'Saturday',
            'Sunday'
        ],
        plotBands: [{ // visualize the weekend
            from: 4.5,
            to: 6.5,
            color: 'rgba(68, 170, 213, .2)'
        }]
    },
    yAxis: {
        title: {
            text: 'Fruit units'
        }
    },
    tooltip: {
        shared: true,
        valueSuffix: ' units'
    },
    credits: {
        enabled: false
    },
    plotOptions: {
        areaspline: {
            fillOpacity: 0.5
        }
    },
    series: [{
        name: 'John',
        data: [3, 4, 3, 5, 4, 10, 12]
    }, {
        name: 'Jane',
        data: [1, 3, 4, 3, 3, 5, 4]
    }]
}

"""

# making a quasar page
def app():
    wp = jp.QuasarPage()
    h1 = jp.QDiv(a=wp, text='Analysis of course reviews', classes='text-h3 text-center q-pa-md')
    p1 = jp.QDiv(a=wp, text='These graphs represents course review analysis')
    
    #getting value from above highcharts value and changing it
    hc = jp.HighCharts(a=wp, options=chart_def)

    hc.options.title.text = 'Average rating of 4 courses'

    hc.options.xAxis.categories = list(month_avg_course.index)

    hc_data = [{"name":v1,"data":[v2 for v2 in month_avg_course[v1]]} for v1 in month_avg_course.columns]
    
    hc.options.series = hc_data

    return wp

jp.justpy(app)