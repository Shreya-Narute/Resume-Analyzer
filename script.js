const uploadForm = document.getElementById('uploadForm');
const resultBox = document.getElementById('result');

uploadForm.addEventListener('submit', function(e) {
    e.preventDefault();
    
    // Fake a processing delay
    setTimeout(() => {
        resultBox.classList.remove('hidden');
        
        document.getElementById('strengths').innerHTML = `<h3>💪 Strengths:</h3><ul><li>Strong communication skills</li><li>Leadership experience</li><li>Technical expertise</li></ul>`;
        
        document.getElementById('weaknesses').innerHTML = `<h3>🛠️ Weaknesses:</h3><ul><li>Need to improve time management</li><li>Limited experience in team projects</li></ul>`;
        
        document.getElementById('recommendations').innerHTML = `<h3>🎯 Recommended Jobs:</h3><ul><li>Software Engineer</li><li>Product Manager</li><li>Business Analyst</li></ul>`;
    }, 2000);
});
