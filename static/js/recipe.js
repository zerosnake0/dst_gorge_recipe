$(function() {
    function refilter() {
        craving = $(".craving_filter.chosen").text()
        station = $(".station_filter.chosen").text()
        coin = $("th.coin.chosen").attr("data-cointype")
        silver_coin = $("th.silver_coin.chosen").attr("data-cointype")
        $("tr.dish").each(function(index){
            if (craving != '' && !$(this).hasClass(craving)) {
                $(this).hide()
                return
            }
            if (station != '' && !$(this).hasClass(station)) {
                $(this).hide()
                return
            }
            if (coin != null) {
                let nc = $(this).find("td.coin[data-cointype='" + coin + "']").text()
                if (nc == '') {
                    $(this).hide()
                    return
                }
            }
            if (silver_coin != null) {
                let nc = $(this).find("td.silver_coin[data-cointype='" + silver_coin + "']").text()
                if (nc == '') {
                    $(this).hide()
                    return
                }
            }
            $(this).show()
         })
    }

    // filter
    function foo(cname) {
        $(cname).click(function(){
            if ($(this).hasClass("chosen")) {
                $(this).removeClass("chosen")
            } else {
                $(cname).removeClass("chosen")
                $(this).addClass("chosen")
            }
            refilter()
        })
    }

    foo(".craving_filter")
    foo(".station_filter")
    foo("th.coin")
    foo("th.silver_coin")
});
