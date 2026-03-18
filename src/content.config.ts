import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const schema = z.object({
  title: z.string(),
  language: z.enum(['de', 'en']).optional(),
  date: z.date().or(z.string()),
  draft: z.boolean().default(false),
  description: z.string().optional(),
  tags: z.array(z.string()).optional(),
  featureImage: z.string().optional(),
});

export const collections = {
  'de': defineCollection({
    loader: glob({ pattern: "**/*.md", base: "./src/content/de" }),
    schema: schema,
  }),
  'en': defineCollection({
    loader: glob({ pattern: "**/*.md", base: "./src/content/en" }),
    schema: schema,
  }),
};