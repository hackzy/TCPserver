function toggleSubMenu(subMenuId) {
    var subMenu = document.getElementById(subMenuId);
    var subMenus = document.getElementsByClassName('sub-menu');

    for (var i = 0; i < subMenus.length; i++) {
        if (subMenus[i].id !== subMenuId) {
            subMenus[i].classList.remove('show');
        }
    }

    subMenu.classList.toggle('show');
}

function showContent(content) {
    var contentElement = document.getElementById('content');
    contentElement.innerHTML = content;
}

// 获取要监测的元素


// 添加点击事件监听器


document.addEventListener('DOMContentLoaded', function() {
    const element = document.getElementById('test');
    element.addEventListener('click', console.log('元素被点击了！'));
    // 在这里放置您要在页面加载完成后执行的代码
    console.log('页面加载完成！');
});