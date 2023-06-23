function get_userId(){
    const LIFF_ID = "1661467943-96Al857l"
    liff.init({
        liffId : LIFF_ID
    })
    .then(() => {

        /* userIdを取得 ----------------------------------------------- */
        liff.getProfile().then(profile => {
            const USER_ID = profile.userId
            document.getElementById("line_id").value = USER_ID
        })
    })
}

get_userId()