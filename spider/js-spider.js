
//在chrome终端 域内发请求
let links = [
]

//生成页数
for (let i=1; i<=24; i++) {
    let link = "" + i + ""
    links.push(link)
}


for (let q=0; q<=links.length; q++) {
    link = links[q]
    fetch(link)
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
        for(let i=8;i<=doc.length;i++) {
            console.log(doc[i].innerText)
        }
    })
}


//域内请求 DOM选择模板
fetch("")
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
        for(let i=8;i<=doc.length;i++) {
            console.log(doc[i].innerText)
        }
    })

//域内请求 json模板
fetch(link)
    .then(function(response) {
        if(response.ok) {
            //读出返回值
            json = response.json()
            return json
        }
    })
    .then(function(json) {
        for(let i=0; i<=json.data.length; i++) {
            let infor = json.data[i].title
            console.log(infor)
        }
    })  

//在chrome终端 直接选取内容
let a = document.querySelectorAll("p")
for(let i=0;i<=a.length;i++){
    let b = a[i].textContent
    if (b.indexOf("身份") != -1) {
        b = b.replace("身份证号码：", "")
        console.log(b)        
    }
};

for(let i=0;i<=a.length;i++){
    let b = a[i].textContent
    if (b.indexOf("、") != -1) {
        console.log(b)        
    }
};



//域内请求 GBK编码
let links = [
]

//生成页数
for (let i=1; i<=24; i++) {
    let link = "" + i + ""
    links.push(link)
}

for (let q=0; q<=links.length; q++) {
    let link = links[q]
    fetch(link)
        .then(res=> res.blob())
        .then(blob => {
            let reader = new FileReader();
            reader.onload = function(e) {
                let text = reader.result;

                let parser=new DOMParser()
                htmlDoc = parser.parseFromString(text, "text/html")

                let doc = htmlDoc.querySelectorAll("img")
                for(let i=0;i<=doc.length;i++) {
                    console.log(doc[i].getAttribute("src"))//.innerText
                }
            }
            reader.readAsText(blob, 'GBK')
        })
}

//querySelectorAll 子选择
a = document.querySelectorAll("ul.meun_list > li") // ">"指选择子元素
