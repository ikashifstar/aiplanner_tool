from src.services.script_generator import ScriptGenerator


def test_generate_script_has_sections():
    generator = ScriptGenerator()
    sections = generator.generate(title="My Title", video_type="explainer")

    assert len(sections) >= 3
    assert all(section.heading for section in sections)
    assert any("My Title" in section.voice_over for section in sections)
