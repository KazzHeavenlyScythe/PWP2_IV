$(document).ready(function () {

    // NOTIFIKASI TOAST
    function showToast(message) {
        $('#toastMessage').text(message);

        bootstrap.Toast.getOrCreateInstance(
            document.getElementById('appToast')
        ).show();
    }

    // PENCARIAN
    function filterCourses() {
        const keyword = $('#searchMK').val().toLowerCase();
        const hari = $('#filterHari').val();
        const jenis = $('#filterJenis').val();

        let found = 0;

        $('.course-item').each(function () {
            const card = $(this);

            const searchMatch =
                card.data('search').includes(keyword);

            const dayMatch =
                !hari || card.data('hari') === hari;

            const typeMatch =
                !jenis || card.data('jenis') === jenis;

            const visible = searchMatch && dayMatch && typeMatch;

            card.toggle(visible);

            if (visible) found++;
        });

        $('#noCourse').toggleClass('d-none', found > 0);
    }

    $('#searchMK, #filterHari, #filterJenis')
        .on('input change', filterCourses);

    // PENGAMBILAN MATA KULIAH AJAX
    $(document).on('click', '.js-ambil-mk', function () {

        const button = $(this);
        const id = button.data('id');

        if (!confirm('Yakin ingin mengambil mata kuliah ini?')) {
            return;
        }

        button.prop('disabled', true)
              .text('Memproses...');

        $.ajax({
            url: '/ambil-matakuliah',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                matakuliah_id: id
            }),

            success: function (response) {
                showToast(response.pesan);

                if (response.status) {
                    setTimeout(function () {
                        location.reload();
                    }, 700);
                } else {
                    button.prop('disabled', false)
                          .text('+ Ambil Mata Kuliah');
                }
            },

            error: function () {
                showToast('Gagal mengambil mata kuliah.');

                button.prop('disabled', false)
                      .text('+ Ambil Mata Kuliah');
            }
        });
    });

});
