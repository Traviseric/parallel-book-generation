"""
Simplified content generator showing the parallel generation concept
Actual implementation has additional complexity for quality and coherence
"""

def lambda_handler(event, context):
    """
    Generates a single chapter independently using global context
    This runs in parallel with other chapter generations
    
    Key insight: This Lambda can run 10+ times concurrently, each
    generating a different chapter with no coordination needed.
    """
    # Extract inputs
    chapter_info = event['chapter_info']
    global_context = event['global_context']
    
    # Key insight: Everything needed is provided upfront
    chapter_prompt = build_chapter_prompt(
        chapter_title=chapter_info['title'],
        chapter_index=chapter_info['index'],
        chapter_outline=chapter_info['outline'],
        global_context=global_context
    )
    
    # Generate chapter content
    # Note: Actual implementation includes retry logic, token management, etc.
    chapter_content = llm_generate(chapter_prompt)
    
    # Store result
    result_key = f"book/{global_context['book_id']}/chapter_{chapter_info['index']}.json"
    store_chapter(result_key, chapter_content)
    
    return {
        'chapter_index': chapter_info['index'],
        'result_key': result_key,
        'status': 'complete'
    }

def build_chapter_prompt(chapter_title, chapter_index, chapter_outline, global_context):
    """
    Build prompt with all necessary context for independent generation
    """
    return f"""
    Generate Chapter {chapter_index}: {chapter_title}
    
    Book Context:
    - Title: {global_context['title']}
    - Overview: {global_context['overview']}
    - Tone: {global_context['tone']}
    - Key Themes: {', '.join(global_context['themes'])}
    
    Chapter Outline:
    {format_outline(chapter_outline)}
    
    Chapter Relations:
    - Previous chapters cover: {global_context['chapter_summaries'][:chapter_index-1]}
    - This chapter should cover: {chapter_outline['key_points']}
    - Following chapters will cover: {global_context['chapter_summaries'][chapter_index:]}
    
    Generate a complete chapter following this outline while maintaining
    consistency with the global context. The chapter should stand alone
    while fitting seamlessly into the overall book structure.
    """