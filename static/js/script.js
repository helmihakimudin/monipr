if (
  localStorage.theme === "dark" ||
  (!("theme" in localStorage) &&
    window.matchMedia("(prefers-color-scheme: dark)").matches)
) {
  document.documentElement.classList.add("dark");
} else {
  document.documentElement.classList.remove("dark");
}

function toggleDarkMode() {
  console.log("tes");
  if (document.documentElement.classList.contains("dark")) {
    document.documentElement.classList.remove("dark");
    localStorage.theme = "light";
  } else {
    document.documentElement.classList.add("dark");
    localStorage.theme = "dark";
  }
}
function openModal(id) {
  getReference();
  document.getElementById(id).classList.remove("hidden");
}
// function closeModal(id) {
//   document.getElementById(id).classList.add("hidden");
// }

function getReference() {
  $.ajax({
    type: "GET",
    url: "/get-reference",
    success: function (response) {
      console.log(response);
      if (response) {
        $("#add_reference_id").val(response);
      }
    },
    error: function (xhr, status, error) {
      console.error("Error fetching reference ID:", error);
    },
  });
}

// support data-modal-toggle attribute
document.querySelectorAll("[data-modal-toggle]").forEach((btn) => {
  btn.addEventListener("click", () => {
    const id = btn.getAttribute("data-modal-target");
    openModal(id);
  });
});

const statusMap = {
  1: { text: "Created", class: "bg-blue-100 text-blue-700", icon: "📝" },
  2: {
    text: "Pending Approval",
    class: "bg-yellow-100 text-yellow-700",
    icon: "⏳",
  },
  3: { text: "Approved", class: "bg-green-100 text-green-700", icon: "✅" },
  4: { text: "Rejected", class: "bg-red-100 text-red-700", icon: "❌" },
  5: { text: "Modified", class: "bg-purple-100 text-purple-700", icon: "✏️" },
  6: { text: "Canceled", class: "bg-gray-200 text-gray-700", icon: "🚫" },
  7: { text: "Processed", class: "bg-indigo-100 text-indigo-700", icon: "📦" },
  8: { text: "Deleted", class: "bg-black text-white", icon: "🗑️" },
  9: { text: "In Process", class: "bg-orange-100 text-orange-700", icon: "🔄" },
  99: {
    text: "Duplicated",
    class: "bg-red-600 text-white font-bold animate-pulse",
    icon: "⚠️",
  },
};

$(document).ready(function () {
  $("#prTable").DataTable({
    processing: true,
    serverSide: true,
    ajax: "/prs/data",
    columns: [
      {
        data: null,
        render: function (data, type, row, meta) {
          return meta.row + meta.settings._iDisplayStart + 1;
        },
      },
      {
        data: "reference_id",
        orderable: false,
        className: "p-2",
        render: function (data) {
          return data || "-";
        },
      },
      {
        data: "date",
        className: "p-2",
        render: function (data) {
          return data || "-";
        },
      },
      {
        data: "requester",
        orderable: false,
        className: "p-2",
        render: function (data) {
          return data || "-";
        },
      },
      {
        data: "pr_number",
        orderable: false,
        className: "p-2",
        render: function (data) {
          return data || "-";
        },
      },
      {
        data: "pr_status",
        orderable: false,
        className: "p-2",
        render: function (data) {
          if (!data || !statusMap[data]) {
            return `<span class="text-gray-400">-</span>`;
          }
          const status = statusMap[data];
          return `
      <span class="px-2 py-1 rounded-full text-xs font-medium ${status.class}">
        ${status.icon} ${status.text}
      </span>
    `;
        },
      },

      {
        data: "id",
        className: "p-2 flex gap-2",
        orderable: false,
        render: function (data, type, row, meta) {
          if (row.pr_status === null) {
            return `
                  <button
                    class="detailBtn flex items-center gap-1 px-3 py-1.5 rounded-lg 
                          bg-slate-500 text-white text-sm font-medium shadow 
                          hover:bg-slate-600 hover:shadow-md active:scale-95 
                          transition-all duration-200" data-key="${row.id}" data-reference_id="${row.reference_id}" data-requester="${row.requester}" data-date="${row.date}" data-prnumber="${row.pr_number}">
                          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" 
                            stroke-width="2" stroke="currentColor" class="w-4 h-4">
                            <path stroke-linecap="round" stroke-linejoin="round" 
                              d="M4 6h16M4 12h16M4 18h16" />
                          </svg>
                    Detail
                  </button>
                  
                  <button 
                    class="editBtn flex items-center gap-1 px-3 py-1.5 rounded-lg 
                          bg-emerald-500 text-white text-sm font-medium shadow 
                          hover:bg-emerald-600 hover:shadow-md active:scale-95 
                          transition-all duration-200" data-key="${row.id}" data-reference_id="${row.reference_id}" data-requester="${row.requester}" data-date="${row.date}"  data-notes="${row.notes}">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" 
                        stroke-width="2" stroke="currentColor" class="w-4 h-4">
                      <path stroke-linecap="round" stroke-linejoin="round" 
                        d="M16.862 4.487l1.65 1.65a2.121 2.121 0 010 3l-8.91 8.91a4 4 0 01-1.414.943l-3.097.966.966-3.097a4 4 0 01.943-1.414l8.91-8.91a2.121 2.121 0 013 0z" />
                    </svg>
                    Edit
                  </button>

                  <a href="#" 
                    class="delete-pr flex items-center gap-1 px-3 py-1.5 rounded-lg 
                            bg-rose-500 text-white text-sm font-medium shadow 
                            hover:bg-rose-600 hover:shadow-md active:scale-95 
                            transition-all duration-200"
                    data-id="${row.id}"
                    data-reference="${row.reference_id}">
                      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" 
                          stroke-width="2" stroke="currentColor" class="w-4 h-4">
                          <path stroke-linecap="round" stroke-linejoin="round" 
                                d="M6 18L18 6M6 6l12 12" />
                      </svg>
                      Delete
                  </a>

                `;
          } else {
            return `
                  <button
                    class="detailBtn flex items-center gap-1 px-3 py-1.5 rounded-lg 
                          bg-slate-500 text-white text-sm font-medium shadow 
                          hover:bg-slate-600 hover:shadow-md active:scale-95 
                          transition-all duration-200" data-key="${row.id}" data-reference_id="${row.reference_id}" data-requester="${row.requester}" data-date="${row.date}" data-prnumber="${row.pr_number}">
                          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" 
                            stroke-width="2" stroke="currentColor" class="w-4 h-4">
                            <path stroke-linecap="round" stroke-linejoin="round" 
                              d="M4 6h16M4 12h16M4 18h16" />
                          </svg>
                    Detail
                  </button>
                  <!--
                  <button 
                    class="editBtn flex items-center gap-1 px-3 py-1.5 rounded-lg 
                          bg-emerald-500 text-white text-sm font-medium shadow 
                          hover:bg-emerald-600 hover:shadow-md active:scale-95 
                          transition-all duration-200" data-key="${row.id}" data-name="${row.name}" data-requester="${row.requester}" data-description="${row.description}"  data-date="${row.date}" data-jumlah="${row.jumlah}" data-unit="${row.unit}" data-url="${row.url}" data-status="${row.status}" data-notes="${row.notes}">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" 
                        stroke-width="2" stroke="currentColor" class="w-4 h-4">
                      <path stroke-linecap="round" stroke-linejoin="round" 
                        d="M16.862 4.487l1.65 1.65a2.121 2.121 0 010 3l-8.91 8.91a4 4 0 01-1.414.943l-3.097.966.966-3.097a4 4 0 01.943-1.414l8.91-8.91a2.121 2.121 0 013 0z" />
                    </svg>
                    Edit
                  </button> -->
                  `;
          }
        },
      },
    ],
  });
});

// $(document).on("click", ".editBtn", function () {
//   let id = $(this).data("key");
//   let reference_id = $(this).data("reference_id");
//   let requester = $(this).data("requester");
//   let date = $(this).data("date");

//   $("#edit_reference_id").val(reference_id);
//   $("#edit_requester").val(requester);
//   $("#edit_date").val(date);

//   $("#editForm").data("pr-id", id);
//   $("#editForm").attr("action", `/update/${id}`);
//   $("#editForm").attr("method", `POST`);

//   $("#editModal").removeClass("hidden");

//   $.ajax({
//     method: "GET",
//     url: `/get-items-data/${id}`,
//     success: function (response) {
//       console.log(response);

//       // looping data item dari response
//       response.data.forEach((item) => {
//         addItemRow("edit-items-container", item);
//       });

//       // buka modal
//       $("#editModal").removeClass("hidden");
//     },
//   });
// });

  // pastikan handler hanya terpasang sekali
  $(document).off("click", ".editBtn").on("click", ".editBtn", function () {
    const id = $(this).data("key");
    const reference_id = $(this).data("reference_id");
    const requester = $(this).data("requester");
    const date = $(this).data("date");

    $("#edit_reference_id").val(reference_id);
    $("#edit_requester").val(requester);
    $("#edit_date").val(date);

    $("#editForm").data("pr-id", id);
    $("#editForm").attr("action", `/update/${id}`);
    $("#editForm").attr("method", `POST`);

    // cancel request sebelumnya kalau ada
    if (currentEditRequest) {
      try { currentEditRequest.abort(); } catch (e) {}
      currentEditRequest = null;
    }

    // pastikan bersih sebelum append (safety: juga clear di success)
    clearItemsContainer('edit-items-container');

    currentEditRequest = $.ajax({
      method: "GET",
      url: `/get-items-data/${id}`,
      success: function (response) {
        // selalu reset di sini agar tidak ada duplikasi
        clearItemsContainer('edit-items-container');

        const items = response.data || [];
        items.forEach(item => addItemRow('edit-items-container', item));

        $("#editModal").removeClass("hidden");
      },
      error: function (xhr, status, err) {
        if (status !== 'abort') console.error("Error fetch items:", err);
      },
      complete: function () {
        currentEditRequest = null;
      }
    });
  });