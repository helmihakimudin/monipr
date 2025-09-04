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
  document.getElementById(id).classList.remove("hidden");
}
function closeModal(id) {
  document.getElementById(id).classList.add("hidden");
}

// support data-modal-toggle attribute
document.querySelectorAll("[data-modal-toggle]").forEach((btn) => {
  btn.addEventListener("click", () => {
    const id = btn.getAttribute("data-modal-target");
    openModal(id);
  });
});

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
      { data: "name", className: "p-2" },
      {
        data: "description",
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
        data: "jumlah",
        className: "p-2",
        render: function (data) {
          return data || "-";
        },
      },
      {
        data: "unit",
        className: "p-2",
        render: function (data) {
          return `<span class="uppercase">${data}</span>` || "-";
        },
      },
      {
        data: "url",
        className: "p-2",
        orderable: false,
        render: function (data) {
          return data
            ? `<a href="${data}" target="_blank" class="text-blue-500 hover:underline">Link</a>`
            : "-";
        },
      },
      { data: "received_date", className: "p-2" },
      {
        data: "status",
        className: "p-2",
        render: function (data) {
          let base = `inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold shadow-sm transition-all duration-200`;
          if (data === "pending") {
            return `<span class="${base} bg-amber-100 text-amber-800 dark:bg-amber-700 dark:text-amber-100">
              <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" fill="none" 
                viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" 
                  d="M6 4h12M6 20h12M8 4v4a4 4 0 008 0V4M8 20v-4a4 4 0 018 0v4" />
              </svg>
              Pending
            </span>`;
          }
          if (data === "approved") {
            return `<span class="${base} bg-emerald-100 text-emerald-800 dark:bg-emerald-700 dark:text-emerald-100">
              <svg class="w-3.5 h-3.5" xmlns="http://www.w3.org/2000/svg" fill="none" 
                viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
              </svg>
              Approved
            </span>`;
          }
          if (data === "rejected") {
            return `<span class="${base} bg-rose-100 text-rose-800 dark:bg-rose-700 dark:text-rose-100">
              <svg class="w-3.5 h-3.5" xmlns="http://www.w3.org/2000/svg" fill="none" 
                viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
              Rejected
            </span>`;
          }
          if (data === "done") {
            return `<span class="${base} bg-sky-100 text-sky-800 dark:bg-sky-700 dark:text-sky-100">
              <svg class="w-3.5 h-3.5" xmlns="http://www.w3.org/2000/svg" fill="none" 
                viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" 
                  d="M9 12l2 2l4-4m6 2a9 9 0 11-18 0a9 9 0 0118 0z" />
              </svg>
              Done
            </span>`;
          }
          return "-";
        },
      },
      {
        data: "notes",
        orderable: false,
        className: "p-2",
        render: function (data) {
          return data || "-";
        },
      },
      {
        data: "id",
        className: "p-2 flex gap-2",
        orderable: false,
        render: function (data, type, row, meta) {
          if (row.status === "pending") {
            return `
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
                  </button>

                  <a href="/delete/${data}" 
                    onclick="return confirm('Yakin hapus PR ini? ${row.name}')"
                    class="flex items-center gap-1 px-3 py-1.5 rounded-lg 
                            bg-rose-500 text-white text-sm font-medium shadow 
                            hover:bg-rose-600 hover:shadow-md active:scale-95 
                            transition-all duration-200">
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
                  </button>`;
          }
        },
      },
    ],
  });
});

$(document).on("click", ".editBtn", function () {
  let id = $(this).data("key");
  let name = $(this).data("name");
  let requester = $(this).data("requester");
  let description = $(this).data("description");
  let date = $(this).data("date");
  let jumlah = $(this).data("jumlah");
  let unit = $(this).data("unit");
  let url = $(this).data("url");
  let status = $(this).data("status");
  let notes = $(this).data("notes");

  $("#edit_name").val(name);
  $("#edit_requester").val(requester);
  $("#edit_description").val(description || "");
  $("#edit_date").val(date);
  $("#edit_jumlah").val(jumlah);
  $("#edit_unit").val(unit);
  $("#edit_url").val(url);
  $("#edit_status").val(status);
  $("#edit_notes").val(notes || "");

  $("#editForm").data("pr-id", id);
  $("#editForm").attr("action", `/update/${id}`);
  $("#editForm").attr("method", `POST`);

  $("#editModal").removeClass("hidden");
});
