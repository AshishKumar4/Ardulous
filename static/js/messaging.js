

function createMsgPanelEntry(data)
{
    var s = "";
    
    s = '<div class="msgContact-recent-box"> <div class="msgContact-recent-pic"> <img class="msgContact-user-pic" src="'+data['profile_pic']+'" /> </div> <div class="msgContact-recent-name"> '+data['name']+' </div> <div class="msgContact-recent-lastMsg"> </div> <div class="msgContact-recent-count"> '+data['stats-unseen']+' </div> </div>';
    
    return s.replace(/undefined/g, "");
}

function createMultiMsgPanelEntries(data)
{
    var dd = JSON.parse(data);
    var s = "";
    for(var i = 0; i < dd.length; i++)
    {
        s += createMsgPanelEntry(dd[i]);
    }
    return s;
}

function refreshMsgGeneralList(count, pos)
{
    var xhttp = new XMLHttpRequest();
    var d = document.getElementById("messaging-general").getElementsByClassName("msgContact-general-board")[0];
    xhttp.onreadystatechange = function () 
    {
        if (this.readyState == 4 && this.status == 200) 
        {
            msgrecent_pos += count;
            d.innerHTML += createMultiMsgPanelEntries(this.responseText);
        }
    };
    xhttp.open("POST", "/handlers/msgGeneralListFetch", true);
    xhttp.send(JSON.stringify({count:count, pos: msgrecent_pos-pos}));
}

var msgrecent_pos = 0;

function refreshMsgRecentList(count, pos)
{
    var xhttp = new XMLHttpRequest();
    var d = document.getElementById("messaging-recent").getElementsByClassName("msgContact-recent-board")[0];
    xhttp.onreadystatechange = function () 
    {
        if (this.readyState == 4 && this.status == 200) 
        {
            msgrecent_pos += count;
            d.innerHTML += createMultiMsgPanelEntries(this.responseText);
        }
    };
    xhttp.open("POST", "/handlers/msgRecentListFetch", true);
    xhttp.send(JSON.stringify({count:count, pos: msgrecent_pos-pos}));
}