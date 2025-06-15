/*!
* Start Bootstrap - Clean Blog v6.0.9 (https://startbootstrap.com/theme/clean-blog)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-clean-blog/blob/master/LICENSE)
*/
window.addEventListener('DOMContentLoaded', () => {
    let scrollPos = 0;
    const mainNav = document.getElementById('mainNav');
    const headerHeight = mainNav.clientHeight;
    window.addEventListener('scroll', function() {
        const currentTop = document.body.getBoundingClientRect().top * -1;
        if ( currentTop < scrollPos) {
            // Scrolling Up
            if (currentTop > 0 && mainNav.classList.contains('is-fixed')) {
                mainNav.classList.add('is-visible');
            } else {
                console.log(123);
                mainNav.classList.remove('is-visible', 'is-fixed');
            }
        } else {
            // Scrolling Down
            mainNav.classList.remove(['is-visible']);
            if (currentTop > headerHeight && !mainNav.classList.contains('is-fixed')) {
                mainNav.classList.add('is-fixed');
            }
        }
        scrollPos = currentTop;
    });

    // HTML要素への参照を取得
    const inputTextElement = document.getElementById('inputText');
    const convertButton = document.getElementById('convertButton');
    const outputElement = document.getElementById('output');

    /**
     * 文字列を変換する関数
     * この関数を自由にカスタマイズしてください。
     * 例: 全て大文字にする、スペースを削除する、特定の文字を置換するなど。
     *
     * @param {string} inputString 入力された文字列
     * @returns {string} 変換後の文字列
     */
    function transformString(inputString) {
        // 例1: 全て大文字に変換
        // return inputString.toUpperCase();

        // 例2: 文字列からすべてのスペースを削除
        // return inputString.replace(/\s/g, '');

        // 例3: 特定の単語を置換 (例: "JavaScript" を "JS" に)
        // return inputString.replace(/JavaScript/g, 'JS');
        const head = '<iframe style="border-radius:12px" src="https://open.spotify.com/embed/episode/'
        const tail = '?utm_source=generator" width="100%" height="352" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>'
        let keyword = inputString.match(/https:\/\/open.spotify.com\/episode\/(.*?)\?/);
        let result = head.concat(keyword[1], tail);

        // 例4: 各単語の最初の文字を大文字にする (タイトルケース)
        // return inputString.split(' ').map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()).join(' ');

        // デフォルト: 何も変換しない (入力そのまま)
        // return inputString;
        return result;
    }

    // 変換ボタンがクリックされた時の処理
    convertButton.addEventListener('click', () => {
        // 入力された文字列を取得
        const inputText = inputTextElement.value;

        // 文字列を変換関数で処理
        const transformedText = transformString(inputText);

        // 変換結果をWebページに出力
        outputElement.textContent = transformedText; // textContentでテキストとして安全に出力
    });

})
