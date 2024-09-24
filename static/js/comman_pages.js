

(function() {
    "use strict";
   // fin1 for blog post
    document.addEventListener("DOMContentLoaded", function () {
            // Function to truncate text after a specified number of words
            function truncateText(element, wordLimit) {
                let fullText = element.innerHTML.trim();
                let words = fullText.split(" ");

                if (words.length > wordLimit) {
                    let visibleText = words.slice(0, wordLimit).join(" ");
                    let hiddenText = words.slice(wordLimit).join(" ");

                    // Create the truncated text with "read more"
                    element.innerHTML = `
                        ${visibleText}
                        <span class="dots">...</span>
                        <span class="more-text" style="display:none;"> ${hiddenText}</span>
                        <span class="read-more"><a herf="#">read more</a></span>
                    `;

                    // Add event listener to toggle full text display
                    if(element.className=='blog-text blog-shortNote-text'){
                        element.querySelector(".read-more").addEventListener("click", function () {
                            const dots = element.querySelector(".dots");
                            const moreText = element.querySelector(".more-text");
                            const readMoreBtn = element.querySelector(".read-more");
        
                            if (dots.style.display === "none") {
                                dots.style.display = "inline";
                                moreText.style.display = "none";
                                readMoreBtn.textContent = "read more";
                            } else {
                                dots.style.display = "none";
                                moreText.style.display = "inline";
                                readMoreBtn.textContent = "read less";
                            }
                        });
                    }
                    
                }
            }

            // Apply the function to all blog text elements
            document.querySelectorAll(".blog_list .blog-text").forEach(function (element) {
                truncateText(element, 23); // Truncate after 15 words
            });
            
            document.querySelectorAll(".blog_list .blog-shortNote-text").forEach(function (element) {
                truncateText(element, 6); // Truncate after 15 words
            });
    });

    // fun2 for 3 comman carousel
    $(document).ready(function(){
        $('.comman_car_list .owl-carousel').owlCarousel({
            loop: true,
            margin: 10, 
            autoplay: true, // Enable auto-loop
            autoplayTimeout: 3000, // Time between each auto-slide (in milliseconds, e.g., 3000ms = 3 seconds)
            autoplayHoverPause: true, // Pause on hover
            responsive: {
                0: {
                    items: 1.5, // 2 cards on small screens (phones)
                    stagePadding: 0, // Show part of the next card
                },
                449: {
                    items: 1.8, // 2 cards on small screens (phones)
                    stagePadding: 5, // Show part of the next card
                },
                689: {
                    items: 2.5, // 3 cards on small tablets
                    stagePadding: 10 // Show part of the next card
                },
                992: {
                    items: 3, // 4 cards on tablets
                    stagePadding: 20 // Show part of the next card
                },
                1200: {
                    items: 4, // 5 cards on large screens (desktops)
                    stagePadding: 2, // Show part of the next card
                    margin: 5, // Margin between cards
                },
                1300: {
                    items: 4.4, // 5 cards on large screens (desktops)
                    stagePadding: 40, // Show part of the next card
                    margin: 10, // Margin between cards
                }
            }
        });
    });


})();