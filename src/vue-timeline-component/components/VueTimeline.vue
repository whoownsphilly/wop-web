<template>
    <div id="timeline2"></div>
</template>

<script>
import * as d3 from 'd3'

import timeline from '../graph/timeline'

export default {
    props: {
        data: {
            type: Array
        },
        divId: {type: String}
    },
    mounted() {
        d3.select("#timeline2")
            .datum(this.data)
            .call(timeline({
                    widthResizable: true,
                    margin: {
                        top: 0,
                        bottom: 30,
                        left: 15,
                        right: 15
                    },
                    //onEventClick: click
                }))
    }
}
</script>
