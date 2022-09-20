const items = document.querySelector(".items");
const searchInstallation = document.querySelector('#recherche');
let installations = []

const fetchInstallations = () => {
  fetch("http://127.0.0.1:5000//api/all-installations")
    .then(res => { res.json()
      .then(res => {
          installations = res;
          showInstallations(installations)
      })
      .catch(err => console.log(err));
    })
    .catch(err => console.log(err));
};

const showInstallations = (installations_) => {
  let sortie = "";

installations_.forEach(({installation, cathegorie}) => (sortie += `
<tr>
  <td class="py-2 pl-5 border-b border-gray-200 bg-white">
  <div class="flex items-center">
    <div class="flex-shrink-0 w-10 h-10">
    <a class="capitalize font-semibold text-base text-gray-900 whitespace-no-wrap"
      href="http://127.0.0.1:5000/installation/information?nom=${installation}&type=${cathegorie}">${installation}
    </a>
    </div>
  </div>
  </td>
</tr>
`));
  items.innerHTML = sortie;
}
document.addEventListener("DOMContentLoaded", fetchInstallations);

searchInstallation.addEventListener('input', e => {
  const element = e.target.value.toLowerCase()
  const newInstallation = installations
    .filter(installation_ => installation_.installation
    .toLowerCase()
    .includes(element))

    showInstallations(newInstallation)
})