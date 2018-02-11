from flask import Flask, render_template

app=Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/plot/')
def plot():
    from pandas_datareader import data
    import datetime
    from bokeh.plotting import figure, show, output_file
    from bokeh.embed import components
    from bokeh.resources import CDN

    start=datetime.datetime(2015,11,1)
    end=datetime.datetime(2016,3,10)

    df=data.DataReader(name="WIKI/GOOG",data_source="quandl", start=start,end=end)

    def inc_dec(o, c):
        if c > o:
            value = 'Increase'
        elif o > c:
            value = 'Decrease'
        else:
            value = 'Equal'
        return value

    df['status'] = [inc_dec(o, c) for o, c in zip(df.Open, df.Close)]

    p=figure(x_axis_type="datetime", width=1000, height=300, sizing_mode='scale_width')
    p.title.text="Candlestick Chart"
    p.grid.grid_line_alpha = 0.3

    hours_12=12*60*60*1000

    p.segment(df.index, df.High, df.index, df.Low, color = "Black")

    p.rect(df.index[df.status == 'Increase'],
           (df.Open[df.status == 'Increase']+df.Close[df.status == 'Increase'])/2,
           hours_12,
           abs(df.Open[df.status == 'Increase']-df.Close[df.status == 'Increase']),
           fill_color="#CCFFFF", line_color="black")
    p.rect(df.index[df.status == 'Decrease'],
           (df.Open[df.status == 'Decrease']+df.Close[df.status == 'Decrease'])/2,
           hours_12,
           abs(df.Open[df.status == 'Decrease']-df.Close[df.status == 'Decrease']),
           fill_color="#FF3333",line_color="black")

    script1, div1 = components(p)
    cdn_js = CDN.js_files[0]
    cdn_css = CDN.css_files[0]
    return render_template("plot.html", script1 = script1, div1 = div1,
    cdn_css=cdn_css, cdn_js=cdn_js)

if __name__=="__main__":
    app.run(debug=True)
