// const IS_PRODUCTION = process.env.NODE_ENV === 'production'

module.exports = {
    outputDir: 'build',
    assetsDir: 'static',
    // baseUrl: IS_PRODUCTION
    // ? 'http://cdn123.com'
    // : '/',
    // For Production, replace set baseUrl to CDN
    // And set the CDN origin to `yourdomain.com/static`
    // Whitenoise will serve once to CDN which will then cache
    // and distribute
    devServer: {
      headers: { "Access-Control-Allow-Origin": "*" },
      proxy: {
        '/api*': {
          // Forward frontend dev server request for /api to django dev server
            target: 'http://' + process.env.DJANGO_HOSTNAME + ':' + process.env.DJANGO_PORT + '/',
        }
      }
    }
  }
