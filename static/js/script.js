$(document).ready(function() {
    var page = 1; // Başlangıç sayfa numarası
    var toolsPerPage = 9; // Her sayfada kaç obje gösterilecek
  
    // Sayfa yüklendiğinde otomatik olarak AJAX isteği yap
    loadTools();
    // AJAX isteği yapmak için bir işlev tanımla
    function loadTools() {
      $.ajax({
        url: "/load_more_tools/", // Django tarafında bu URL'yi tanımlamanız gerekiyor
        method: "GET",
        data: {
          page: page,
          per_page: toolsPerPage
        },
        success: function(data) {
          if (data.length > 0) {
            // Gelen verileri mevcut sayfaya ekleyin
            $("#tool-list").append(data);
            page += 1; // Sayfa numarasını artırın
          } else {
            $("#load-more").hide(); // Eklenecek daha fazla veri yoksa butonu gizle
          }
        }
      });
    }
  });
  