-- AI Prompt Optimizer Database Initialization
-- This script creates the initial database schema and sample data

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create sample templates
INSERT INTO templates (name, description, template_content, category, industry, tags, usage_count, average_rating, is_public, is_featured, difficulty_level, estimated_tokens, optimization_potential, author, version) VALUES
(
    'Marketing Copy Generator',
    'Generate compelling marketing copy for products and services',
    'Create a {tone} marketing copy for {product/service} that targets {audience}. The copy should highlight {key_features} and include a call-to-action. Keep it under {word_limit} words.',
    'marketing',
    'general',
    '["marketing", "copywriting", "sales"]',
    150,
    4.5,
    true,
    true,
    'beginner',
    45,
    0.35,
    'AI Prompt Optimizer Team',
    '1.0'
),
(
    'Code Review Assistant',
    'Get detailed code review and improvement suggestions',
    'Review this {programming_language} code and provide feedback on: 1) Code quality and best practices 2) Performance optimizations 3) Security considerations 4) Readability improvements. Code: {code_snippet}',
    'coding',
    'technology',
    '["programming", "code-review", "development"]',
    89,
    4.7,
    true,
    true,
    'intermediate',
    78,
    0.42,
    'AI Prompt Optimizer Team',
    '1.0'
),
(
    'Content Summarizer',
    'Summarize long-form content while preserving key information',
    'Summarize the following {content_type} in {summary_length} words. Focus on the main points and key insights. Maintain the original tone and include any important data or statistics. Content: {content}',
    'writing',
    'general',
    '["summarization", "content", "writing"]',
    234,
    4.3,
    true,
    false,
    'beginner',
    52,
    0.28,
    'AI Prompt Optimizer Team',
    '1.0'
),
(
    'Business Plan Generator',
    'Create comprehensive business plans for startups and projects',
    'Generate a business plan for {business_type} that includes: 1) Executive Summary 2) Market Analysis 3) Competitive Analysis 4) Marketing Strategy 5) Financial Projections 6) Risk Assessment. Target market: {target_market}',
    'business',
    'entrepreneurship',
    '["business", "planning", "strategy"]',
    67,
    4.6,
    true,
    true,
    'advanced',
    120,
    0.38,
    'AI Prompt Optimizer Team',
    '1.0'
),
(
    'Email Response Generator',
    'Create professional email responses for various scenarios',
    'Write a {tone} email response to: {email_context}. The response should be {length} and address {key_points}. Include appropriate greetings and closings.',
    'communication',
    'general',
    '["email", "communication", "professional"]',
    189,
    4.4,
    true,
    false,
    'beginner',
    38,
    0.31,
    'AI Prompt Optimizer Team',
    '1.0'
),
(
    'Data Analysis Report',
    'Generate comprehensive data analysis reports',
    'Analyze the following dataset and create a report covering: 1) Key insights and trends 2) Statistical summary 3) Visualizations recommendations 4) Actionable recommendations. Dataset: {data_description}',
    'analytics',
    'data-science',
    '["analytics", "data", "reporting"]',
    45,
    4.8,
    true,
    true,
    'advanced',
    95,
    0.45,
    'AI Prompt Optimizer Team',
    '1.0'
),
(
    'Creative Story Generator',
    'Generate creative stories and narratives',
    'Write a {genre} story about {main_character} who {plot_element}. The story should be {length} and include {story_elements}. Make it engaging and original.',
    'creative',
    'entertainment',
    '["creative", "storytelling", "narrative"]',
    156,
    4.2,
    true,
    false,
    'intermediate',
    85,
    0.33,
    'AI Prompt Optimizer Team',
    '1.0'
),
(
    'Technical Documentation',
    'Create clear and comprehensive technical documentation',
    'Write technical documentation for {system/feature} that includes: 1) Overview and purpose 2) Installation/setup instructions 3) Usage examples 4) API reference 5) Troubleshooting guide. Target audience: {audience}',
    'documentation',
    'technology',
    '["documentation", "technical", "guide"]',
    78,
    4.6,
    true,
    true,
    'intermediate',
    110,
    0.40,
    'AI Prompt Optimizer Team',
    '1.0'
);

-- Create sample users (for testing)
-- Note: In production, these would be created through the registration process
INSERT INTO users (email, hashed_password, first_name, last_name, is_active, is_verified, subscription_tier, monthly_optimizations, optimizations_used, monthly_tokens, tokens_used, created_at) VALUES
(
    'demo@aipromptoptimizer.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.iK8i', -- password: demo123
    'Demo',
    'User',
    true,
    true,
    'pro',
    1000,
    45,
    50000,
    2300,
    NOW() - INTERVAL '30 days'
),
(
    'test@aipromptoptimizer.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.iK8i', -- password: demo123
    'Test',
    'User',
    true,
    true,
    'free',
    50,
    12,
    10000,
    800,
    NOW() - INTERVAL '15 days'
);

-- Create sample prompts
INSERT INTO prompts (user_id, original_prompt, optimized_prompt, prompt_type, title, description, tags, category, original_tokens, optimized_tokens, token_reduction_percentage, clarity_score, specificity_score, overall_quality_score, status, created_at) VALUES
(
    1,
    'Write a comprehensive marketing email for our new AI-powered productivity tool that helps teams collaborate better and includes features like real-time editing, task management, and analytics. The email should be engaging and persuasive, targeting business professionals and managers who are looking to improve their team efficiency.',
    'Create a compelling marketing email for our AI productivity tool. Target: business professionals seeking team efficiency. Highlight: real-time editing, task management, analytics. Tone: engaging, persuasive.',
    'text',
    'AI Productivity Tool Marketing Email',
    'Marketing email for AI-powered productivity tool',
    '["marketing", "email", "productivity"]',
    'marketing',
    89,
    45,
    49.4,
    8.2,
    7.8,
    8.0,
    'completed',
    NOW() - INTERVAL '5 days'
),
(
    1,
    'I need help writing a Python function that takes a list of numbers and returns the sum of all even numbers in the list. The function should be efficient and include proper error handling for edge cases like empty lists or non-numeric values.',
    'Write a Python function to sum even numbers from a list. Include error handling for empty lists and non-numeric values.',
    'code',
    'Python Even Numbers Sum Function',
    'Python function to sum even numbers with error handling',
    '["python", "function", "error-handling"]',
    'coding',
    67,
    32,
    52.2,
    9.1,
    8.9,
    9.0,
    'completed',
    NOW() - INTERVAL '3 days'
),
(
    2,
    'Can you help me write a professional email to my boss explaining why I need to take next Friday off for a family emergency? I want to be respectful and professional while explaining the situation.',
    'Write a professional email requesting Friday off for a family emergency.',
    'text',
    'Time Off Request Email',
    'Professional email requesting time off',
    '["email", "professional", "time-off"]',
    'communication',
    45,
    23,
    48.9,
    7.5,
    6.8,
    7.2,
    'completed',
    NOW() - INTERVAL '1 day'
);

-- Create sample optimizations
INSERT INTO optimizations (prompt_id, user_id, optimization_type, model_used, original_prompt, optimized_prompt, original_tokens, optimized_tokens, token_reduction, token_reduction_percentage, quality_score, clarity_score, specificity_score, original_cost, optimized_cost, cost_savings, cost_savings_percentage, optimization_notes, processing_time, created_at) VALUES
(
    1,
    1,
    'token_reduction',
    'gpt-4',
    'Write a comprehensive marketing email for our new AI-powered productivity tool that helps teams collaborate better and includes features like real-time editing, task management, and analytics. The email should be engaging and persuasive, targeting business professionals and managers who are looking to improve their team efficiency.',
    'Create a compelling marketing email for our AI productivity tool. Target: business professionals seeking team efficiency. Highlight: real-time editing, task management, analytics. Tone: engaging, persuasive.',
    89,
    45,
    44,
    49.4,
    8.0,
    8.2,
    7.8,
    0.00267,
    0.00135,
    0.00132,
    49.4,
    'Successfully reduced token count by 49.4% while maintaining all key information and improving clarity.',
    2.3,
    NOW() - INTERVAL '5 days'
),
(
    2,
    1,
    'token_reduction',
    'gpt-4',
    'I need help writing a Python function that takes a list of numbers and returns the sum of all even numbers in the list. The function should be efficient and include proper error handling for edge cases like empty lists or non-numeric values.',
    'Write a Python function to sum even numbers from a list. Include error handling for empty lists and non-numeric values.',
    67,
    32,
    35,
    52.2,
    9.0,
    9.1,
    8.9,
    0.00201,
    0.00096,
    0.00105,
    52.2,
    'Excellent token reduction achieved while preserving all technical requirements.',
    1.8,
    NOW() - INTERVAL '3 days'
),
(
    3,
    2,
    'clarity_improvement',
    'gpt-3.5-turbo',
    'Can you help me write a professional email to my boss explaining why I need to take next Friday off for a family emergency? I want to be respectful and professional while explaining the situation.',
    'Write a professional email requesting Friday off for a family emergency.',
    45,
    23,
    22,
    48.9,
    7.2,
    7.5,
    6.8,
    0.000675,
    0.000345,
    0.00033,
    48.9,
    'Improved clarity and conciseness while maintaining professional tone.',
    1.5,
    NOW() - INTERVAL '1 day'
);

-- Create sample analytics
INSERT INTO analytics (user_id, date, total_optimizations, total_tokens_processed, total_tokens_saved, total_cost, total_cost_savings, average_optimization_time, average_token_reduction, average_quality_score, model_usage, optimization_type_usage, successful_optimizations, failed_optimizations, created_at) VALUES
(
    1,
    CURRENT_DATE - INTERVAL '5 days',
    1,
    89,
    44,
    0.00267,
    0.00132,
    2.3,
    49.4,
    8.0,
    '{"gpt-4": 1}',
    '{"token_reduction": 1}',
    1,
    0,
    NOW() - INTERVAL '5 days'
),
(
    1,
    CURRENT_DATE - INTERVAL '3 days',
    1,
    67,
    35,
    0.00201,
    0.00105,
    1.8,
    52.2,
    9.0,
    '{"gpt-4": 1}',
    '{"token_reduction": 1}',
    1,
    0,
    NOW() - INTERVAL '3 days'
),
(
    2,
    CURRENT_DATE - INTERVAL '1 day',
    1,
    45,
    22,
    0.000675,
    0.00033,
    1.5,
    48.9,
    7.2,
    '{"gpt-3.5-turbo": 1}',
    '{"clarity_improvement": 1}',
    1,
    0,
    NOW() - INTERVAL '1 day'
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_prompts_user_id ON prompts(user_id);
CREATE INDEX IF NOT EXISTS idx_prompts_status ON prompts(status);
CREATE INDEX IF NOT EXISTS idx_prompts_created_at ON prompts(created_at);
CREATE INDEX IF NOT EXISTS idx_optimizations_user_id ON optimizations(user_id);
CREATE INDEX IF NOT EXISTS idx_optimizations_prompt_id ON optimizations(prompt_id);
CREATE INDEX IF NOT EXISTS idx_optimizations_created_at ON optimizations(created_at);
CREATE INDEX IF NOT EXISTS idx_analytics_user_id ON analytics(user_id);
CREATE INDEX IF NOT EXISTS idx_analytics_date ON analytics(date);
CREATE INDEX IF NOT EXISTS idx_templates_category ON templates(category);
CREATE INDEX IF NOT EXISTS idx_templates_is_featured ON templates(is_featured);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_subscription_tier ON users(subscription_tier); 