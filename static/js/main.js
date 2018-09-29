function createMiniProfileCard(data)
{
    var s = "";
    
    s = '<div class="wrapper"> <div class="profile-card js-profile-card"> <div class="profile-card__img"> <img src="'+data['profile_pic']+'" alt="profile card"> </div> <div class="profile-card__cnt js-profile-cnt"> <div class="profile-card__name">'+data['name']+'</div> <div class="profile-card__txt">'+data['info']+'</div> <div class="profile-card-loc"> <span class="profile-card-loc__icon"> <svg class="icon"> <use xlink:href="#icon-location"></use> </svg> </span> <span class="profile-card-loc__txt"> '+data['city']+' </span> </div> <div class="profile-card-inf"> <div class="profile-card-inf__item"> <div class="profile-card-inf__title">'+data['stats']['followers']+'</div> <div class="profile-card-inf__txt">Followers</div> </div> <div class="profile-card-inf__item"> <div class="profile-card-inf__title">'+data['stats']['following']+'</div> <div class="profile-card-inf__txt">Following</div> </div> <div class="profile-card-inf__item"> <div class="profile-card-inf__title">'+data['stats']['posts']+'</div> <div class="profile-card-inf__txt">Posts</div> </div> <!-- <div class="profile-card-inf__item"> <div class="profile-card-inf__title">85</div> <div class="profile-card-inf__txt">Works</div> </div> --> </div> <div class="profile-card-ctr"> <button class="profile-card__button button--blue js-message-btn">Message</button> <button class="profile-card__button button--orange" onclick="makeFollowToUser(\''+data['id']+'\');">Follow</button> </div> </div> </div> </div>';//'<div class="container posts"> <div class="post-header container"> <div class="post-author-card"> <div class="post-author"> <div class="post-author-pic"><img class="post-author-pic-img" src="'+data['author-pic']+'" /></div> <div class="post-author-name"> '+data['author-name']+' </div> </div> </div> <div class="post-datetime"> '+data['time']+' </div> </div> <div class="post-body container"> <div class="post-text"> '+data['text']+' </div> </div> <div class="post-interactions container"> <div class="post-like-button"> <div class="glyphicon glyphicon-heart-empty"></div> '+data['stats-likes']+' </div> <div class="post-comment-button"> <div class="glyphicon glyphicon-comment"></div> '+data['stats-comments']+' </div> <div class="post-share-button"> <div class="glyphicon glyphicon-share"></div> '+data['stats-shares']+' </div> </div> <div class="post-comments container"> </div> </div> ';
    
    return s.replace(/undefined/g, "");
}

function createMultiMiniProfileCards(data)
{
    var dd = JSON.parse(data);
    var s = "";
    if(dd['type'] == 'user')
    {
        for(var i = 0; i < dd['data'].length; i++)
        {
            s += createMiniProfileCard(dd['data'][i]);
        }
    }
    else 
    {

    }
    return s;
}

function loadMiniProfileCards(obj, type)
{
    var dd = document.getElementById("wall");
    dd.innerHTML += "<br><br>Sorted by "+type+"<br><br>" + createMultiMiniProfileCards(obj);
}   

function makeFollowToUser(uid)
{
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () 
    {
        if (this.readyState == 4 && this.status == 200) 
        {
            //feedpos += fetchCount;
            //d.innerHTML = createMultiPostCards(this.responseText);
            alert("You are now following the User!");
        }
    };
    xhttp.open("POST", "/handlers/makefollow", true);
    xhttp.send(JSON.stringify({uid: uid}));
}