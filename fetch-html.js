fetch("url")
    .then(function(response) {
        if(response.ok) {
            //读出返回值
            text = response.text()
            return text
        }
    })
    .then(function(text) {
        //将返回的html字符串解析为一个 DOM Document
        let parser=new DOMParser()
        htmlDoc = parser.parseFromString(text, "text/html")
        
        let doc = htmlDoc.querySelectorAll("tr")
        for(let i=8;i<30;i++) {
            console.log(doc[i].innerText)
        }
    })
